XGallery
========

XGallery is a project to manage image galleries in a Django application.  It's
integrated with the XBlog and XComments applications, and includes legacy
the Gallery2 API.

It's a bit rough around the edges, and has support for some things that just
don't exist any more, like:

- Photocast: I don't think Apple does this any more
- Gallery2 API: Gallery2 used to be popular and there were clients
- Flash: Remember flash?
- PicLens: pretty neat old gallery plugin, but nobody uses plugins any more

If you want to try it out,  install [Django](https://djangoproject.com) and
add the `django-xgallery` directory to your PYTHONPATH. Alternately, symlink
the `xgallery` subdirectory to your Django installation (same directory as
`manage.py`).

To-Do:

- drop gallery2 support: this was only in because there was a plug-in for
  early versions of iPhoto that uploaded to gallery2 (php) servers. it
worked okay and no regerts

- add lightGallery display; this looks like a pretty neat little frontend
  that I definitely don't feel like trying to rip off

- integrate with WP api, so the client app can upload and have a pic chooser
  (will probably need to strip some stuff out of xblog for that)
