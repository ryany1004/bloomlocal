import uuid

from django.utils.text import slugify


def unique_slug_filename(filename):
    path_file = filename.split('.')
    ext = path_file.pop()
    name = u"".join(path_file)

    prefix = str(uuid.uuid1())[:4]
    file_name = u'%s__%s.%s' % (prefix, slugify(name), ext)

    return file_name


def get_photo_path(instance, filename= ''):
    random_str = str(uuid.uuid1())[:8]
    filename = f"product/{random_str}/{unique_slug_filename(filename)}"
    return filename

def get_shop_path(instance, filename= ''):
    random_str = str(uuid.uuid1())[:8]
    filename = f"shop/{random_str}/{unique_slug_filename(filename)}"
    return filename
