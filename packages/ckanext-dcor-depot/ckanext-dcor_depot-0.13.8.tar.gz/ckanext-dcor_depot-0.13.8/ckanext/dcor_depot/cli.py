import datetime
import pathlib
import time
import traceback as tb

import ckan.logic as logic
import ckan.model as model
import click

from dcor_shared import (
    DC_MIME_TYPES, s3, get_ckan_config_option, get_resource_path, sha256sum)

from . import app_res
from .depotize import depotize
from .figshare import figshare
from .internal import internal, internal_upgrade
from . import jobs


def click_echo(message, am_on_a_new_line):
    if not am_on_a_new_line:
        click.echo("")
    click.echo(message)


@click.command()
@click.argument('path')
@click.argument('dataset_id')
@click.option('--delete-source', is_flag=True,
              help='Delete the original local file')
def append_resource(path, dataset_id, delete_source=False):
    """Append a resource to a dataset

    This can be done even after the dataset is made active.
    It can be used to e.g. append post-processed RT-DC data to an
    existing dataset.

    Pass the path `path` to a resource, and it will be added to the
    specified `dataset_id` (id or name).
    """
    path = pathlib.Path(path)
    app_res.append_resource(path=path,
                            dataset_id=dataset_id,
                            copy=not delete_source)


@click.command()
@click.argument('dataset_id')
def dcor_list_s3_objects_for_dataset(dataset_id):
    """List S3 resource and other data locations for a dataset

    The resources are printed as "bucket:path (message)" and the
    colors indicate whether the object is publicly available (green),
    private (blue), or not there (red).
    """
    package_show = logic.get_action("package_show")
    dataset_dict = package_show(context={'ignore_auth': True,
                                         'user': 'default'},
                                data_dict={"id": dataset_id})
    # For each resource, list the objects that are currently in S3 along
    # with the S3 object tags.
    circle_id = dataset_dict["organization"]["id"]
    bucket_schema = get_ckan_config_option("dcor_object_store.bucket_name")
    bucket_name = bucket_schema.format(organization_id=circle_id)
    for res_dict in dataset_dict["resources"]:
        rid = res_dict["id"]
        paths = [f"resource/{rid[:3]}/{rid[3:6]}/{rid[6:]}"]
        if res_dict["mimetype"] in DC_MIME_TYPES:
            paths.append(f"condensed/{rid[:3]}/{rid[3:6]}/{rid[6:]}")
            paths.append(f"preview/{rid[:3]}/{rid[3:6]}/{rid[6:]}")
        s3_client, _, _ = s3.get_s3()
        for pp in paths:
            try:
                response = s3_client.get_object_tagging(
                    Bucket=bucket_name,
                    Key=pp)
                tags = []
                for item in response["TagSet"]:
                    tags.append(f"{item['Key']}={item['Value']}")
                if tags.count("public=true"):
                    # As mentioned in the s3 submodule, we define public
                    # access by the presence of the "public=true" tag for
                    # an object.
                    color = "green"
                else:
                    color = "blue"
                    tags.append("PRIVATE")
                message = " ".join(tags)
            except s3_client.exceptions.NoSuchKey:
                color = "red"
                message = "not found"
            click.secho(f"{bucket_name}:{pp} ({message})", fg=color)


@click.command()
@click.option("--modified-days", default=-1,
              help="Only migrate datasets modified within this number of days "
                   + "in the past. Set to -1 to apply to all datasets.")
@click.option("--delete-after-migration", is_flag=True,
              help="Delete files from local block storage after successful "
                   "transfer to object storage.")
@click.option("--verify-existence", is_flag=True,
              help="Verify that resources exist in S3")
@click.option("--verify-checksum", is_flag=True,
              help="Verify the checksum of the file in S3; this option "
                   "implies --verify-existence")
def dcor_migrate_resources_to_object_store(modified_days=-1,
                                           delete_after_migration=False,
                                           verify_existence=False,
                                           verify_checksum=False,
                                           ):
    """Migrate resources on block storage to an S3-compatible object store

    This also happens for draft datasets.
    """
    # verify_checksum implies verify_existence [sic]
    verify_existence = verify_existence or verify_checksum
    # go through all datasets
    datasets = model.Session.query(model.Package)

    if modified_days >= 0:
        # Search only the last `days` days.
        past = datetime.date.today() - datetime.timedelta(days=modified_days)
        past_str = time.strftime("%Y-%m-%d", past.timetuple())
        datasets = datasets.filter(model.Package.metadata_modified >= past_str)

    nl = False
    for dataset in datasets:
        nl = False
        click.echo(f"Migrating dataset {dataset.id}\r", nl=False)
        ds_dict = dataset.as_dict()
        ds_dict["organization"] = logic.get_action("organization_show")(
                context={"user": ds_dict["creator_user_id"]},
                data_dict={"id": dataset.owner_org})
        for resource in dataset.resources:
            res_dict = resource.as_dict()
            rid = res_dict["id"]
            ploc = str(get_resource_path(rid))
            # Get bucket and object names
            bucket_name = get_ckan_config_option(
                "dcor_object_store.bucket_name").format(
                organization_id=ds_dict["organization"]["id"])
            objects = [(ploc,
                        f"resource/{rid[:3]}/{rid[3:6]}/{rid[6:]}",
                        res_dict.get("sha256"))]
            # condensed dataset
            pcond = ploc + "_condensed.rtdc"
            if pathlib.Path(pcond).exists():
                objects.append((pcond,
                                f"condensed/{rid[:3]}/{rid[3:6]}/{rid[6:]}",
                                None))
            # preview image
            pprev = ploc + "_preview.jpg"
            if pathlib.Path(pprev).exists():
                objects.append((pprev,
                                f"preview/{rid[:3]}/{rid[3:6]}/{rid[6:]}",
                                None))
            if not res_dict.get("s3_available") or verify_existence:
                # Upload the resource and condensed file to S3
                for object_path, object_name, sha in objects:
                    sha = sha or sha256sum(object_path)
                    override = False  # no override by default

                    if verify_checksum and s3.object_exists(
                            bucket_name=bucket_name, object_name=object_name):
                        s3_sha256 = s3.compute_checksum(
                            bucket_name=bucket_name,
                            object_name=object_name)
                        if s3_sha256 != sha:
                            # Override only if the user requested it and
                            # only if the SHA256 sum did not match.
                            override = True

                    try:
                        s3_url = s3.upload_file(
                            bucket_name=bucket_name,
                            object_name=object_name,
                            path=object_path,
                            sha256=sha,
                            private=ds_dict["private"],
                            override=override,
                        )
                        if verify_checksum:
                            click_echo(f"Verified {object_name}", nl)
                        elif verify_existence:
                            click_echo(f"Checked {object_name}", nl)
                        else:
                            click_echo(f"Uploaded {object_name}", nl)
                        nl = True
                    except FileNotFoundError:
                        click_echo(f"Missing file {object_path}", nl)
                        nl = True
                    else:
                        # Check if the s3 URLs have been set
                        if ("s3_available" not in res_dict
                                or "s3_url" not in res_dict):
                            try:
                                # Update the resource dictionary
                                logic.get_action("resource_patch")(
                                    context={
                                        # https://github.com/ckan/
                                        # ckan/issues/7787
                                        "user": ds_dict["creator_user_id"],
                                        "ignore_auth": True},
                                    data_dict={"id": rid,
                                               "s3_available": True,
                                               "s3_url": s3_url})
                            except BaseException:
                                click_echo(
                                    f"Failed resource {resource.name}", nl)
                                nl = True
                                click_echo(tb.format_exc(), nl)
                            else:
                                # Just set these here so in the next iteration
                                # (for the condensed file), we don't update
                                # the resource dictionary again.
                                res_dict["s3_available"] = True
                                res_dict["s3_url"] = s3_url
            if delete_after_migration:
                raise NotImplementedError("Deletion not implemented yet!")

    if not nl:
        click.echo("")
    click.echo("Done!")


@click.command()
@click.argument('path')
@click.option('--ignore-unknown', is_flag=True,
              help='Continue when encountering unknown files')
@click.option('--no-cleanup', is_flag=True, help='By default, temporary files '
              + 'are cleaned up, which involves: removing untarred files, '
              + 'moving source tar files to /data/archive/processed/, '
              + 'and archiving processing-metadata in '
              + '/data/archive/archived_meta. Set this flag if you do not '
              + 'want these things to happen.')
@click.option('--skip-failed', is_flag=True,
              help='Skip archives that failed in previous runs')
@click.option('--verbosity', default=1, type=int,
              help='Increase for more verbosity')
def depotize_archive(path, no_cleanup=False, ignore_unknown=False,
                     skip_failed=False, verbosity=1):
    """Transform arbitrary RT-DC data to the DCOR depot file structure

    The following tasks are performed:

    - unpack the tar file to `original/path/filename.tar_depotize/data`
    - scan the unpacked directory for RT-DC data (.rtdc and .tdms);
      found datasets are written to the text file
      `original/path/filename.tar_depotize/measurements.txt`
    - check whether the data files in `measurements.txt` are valid
      and store them in `check_usable.txt`
    - convert the data to compressed .rtdc files and create condensed
      datasets

    By default, the depot data are stored in the directory root in
    `/data/depots/internal/` and follow the directory structure
    `201X/2019-08/20/2019-08-20_1126_c083de*` where the allowed file names
    in this case are

    - 2019-08-20_1126_c083de.sha256sums a file containing SHA256 sums
    - 2019-08-20_1126_c083de_v1.rtdc the actual measurement
    - 2019-08-20_1126_c083de_v1_condensed.rtdc the condensed dataset
    - 2019-08-20_1126_c083de_ad1_m001_bg.png an ancillary image
    - 2019-08-20_1126_c083de_ad2_m002_bg.png another ancillary image

    You may run this command for individual archives:

       ckan depotize-archive /path/to/archive.tar

    or recursively for entire directory trees

       ckan depotize-archive /path/to/directory/
    """
    depotize(path,
             cleanup=not no_cleanup,
             abort_on_unknown=not ignore_unknown,
             skip_failed=skip_failed,
             verbose=verbosity)


@click.command()
@click.option('--limit', default=0, help='Limit number of datasets imported')
def import_figshare(limit):
    """Import a predefined list of datasets from figshare"""
    figshare(limit=limit)


@click.command()
@click.option('--limit', default=0, help='Limit number of datasets imported')
@click.option('--start-date', default="2000-01-01",
              help='Import datasets in the depot starting from a given date')
@click.option('--end-date', default="3000-01-01",
              help='Import datasets in the depot only until a given date')
def import_internal(limit, start_date="2000-01-01", end_date="3000-01-01"):
    """Import internal data located in /data/depots/internal"""
    internal(limit=limit, start_date=start_date, end_date=end_date)


@click.command()
def list_all_resources():
    """List all (public and private) resource ids"""
    datasets = model.Session.query(model.Package)
    for dataset in datasets:
        for resource in dataset.resources:
            click.echo(resource.id)


@click.command()
@click.option('--modified-days', default=-1,
              help='Only run for datasets modified within this number of days '
                   + 'in the past. Set to -1 to apply to all datasets.')
def run_jobs_dcor_depot(modified_days=-1):
    """Compute condensed resource all .rtdc files

    This also happens for draft datasets.
    """
    # go through all datasets
    datasets = model.Session.query(model.Package)

    if modified_days >= 0:
        # Search only the last `days` days.
        past = datetime.date.today() - datetime.timedelta(days=modified_days)
        past_str = time.strftime("%Y-%m-%d", past.timetuple())
        datasets = datasets.filter(model.Package.metadata_modified >= past_str)

    nl = False  # new line character
    for dataset in datasets:
        nl = False
        click.echo(f"Checking dataset {dataset.id}\r", nl=False)
        usr_id = dataset.creator_user_id
        ds_dict = dataset.as_dict()
        ds_dict["organization"] = logic.get_action("organization_show")(
                {'ignore_auth': True}, {"id": dataset.owner_org})
        for resource in dataset.resources:
            res_dict = resource.as_dict()
            try:
                if jobs.symlink_user_dataset(pkg=ds_dict,
                                             usr={"name": usr_id},
                                             resource=res_dict):
                    click_echo(f"Created symlink for {resource.name}", nl)
                    nl = True
            except KeyboardInterrupt:
                raise
            except BaseException as e:
                click_echo(
                    f"{e.__class__.__name__}: {e} for {resource.name}", nl)
                nl = True
    if not nl:
        click.echo("")
    click.echo("Done!")


@click.command()
@click.option('--start-date', default="2000-01-01",
              help='Search for upgraded resources in the depot starting '
                   + 'from a given date')
@click.option('--end-date', default="3000-01-01",
              help='Search for upgraded resources in the depot '
                   + 'only until a given date')
def upgrade_internal(start_date="2000-01-01", end_date="3000-01-01"):
    """Upgrade resource versions located in /data/depots/internal in CKAN

    If you are running this command, you should have already created
    new versions of resources (i.e. date-something_v2.rtdc next to
    a date-something_v1.rtdc file).

    During upgrade, the condensed version of the resource
    (date-something_v2_condensed.rtdc) will be created and the SHA256
    sums file will be updated. Then, the resource will be added to
    the original dataset.
    """
    internal_upgrade(start_date=start_date, end_date=end_date)


def get_commands():
    return [append_resource,
            dcor_list_s3_objects_for_dataset,
            dcor_migrate_resources_to_object_store,
            depotize_archive,
            import_figshare,
            import_internal,
            list_all_resources,
            run_jobs_dcor_depot,
            upgrade_internal,
            ]
