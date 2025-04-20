XGallery
========

XGallery is a project o show image galleries in a django application.  It's integrated with the XBlog and XComments applications, and includes legacy the Gallery2 API. 

To-Do:

- drop gallery2 support: this was only in because there was a plug-in for
  early versions of iPhoto that uploaded to gallery2 (php) servers. it
worked okay and no regerts

- add lightGallery display; this looks like a pretty neat little frontend
  that I definitely don't feel like trying to rip off

- integrate with WP api, so the client app can upload and have a pic chooser
  (will probably need to strip some stuff out of xblog for that)
