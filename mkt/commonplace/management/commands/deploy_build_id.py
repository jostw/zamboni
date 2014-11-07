import logging
import os
import sys
from optparse import make_option

from django.conf import settings
from django.core.files.storage import default_storage as storage
from django.core.management.base import BaseCommand

from mkt.commonplace.models import DeployBuildId


log = logging.getLogger('commonplace')


class Command(BaseCommand):
    def handle(self, *args, **kw):
        if not args and not args[0]:
            sys.stdout.write('Pass repo name as arg (e.g., fireplace).\n')
            sys.exit(1)
        repo = args[0]

        repo_build_id = DeployBuildId.objects.get_or_create(repo=repo)[0]
        old_build_id = repo_build_id.build_id

        # Read the build ID from build_id.txt in the repository's root.
        build_id_path = os.path.join(settings.MEDIA_ROOT, repo, 'build_id.txt')
        with storage.open(build_id_path) as f:
            repo_build_id.build_id = f.read()

        # Save it.
        repo_build_id.save()
        print "Successfully changed %s's build_id from %s to %s in db\n" % (
            repo, old_build_id, repo_build_id.build_id
        )
