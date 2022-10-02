# Django in 5 mins

Django is a web framework written in python, it provides many tools and
librarys that help you do common tasks. It's very easy to learn and quick to
get started 

Django generally is used to make websites that require a database, instagram
uses django for example. 

Let's just get  started and learn by example with a simple application, we will make a very simple blog website.

I'm going to make the assumption that you have python installed on your system. First we should create a virtual enviroment and install django into it.

```
python -m venv venv
source venv/bin/activate
pip install django
```

Now that django is installed, we will have access to the django admin command
which we will use to start our project.

I'll just call this project mywebsite

```
django-admin startproject mywebsite
```

This has created a structure for the project for us:

```
mywebsite/
├── manage.py
└── mywebsite
    ├── asgi.py
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

First we have a root directory if our project, called mywebsite, everything
lives in here.

`manage.py` is our way of controlling django from the command line

Our next mywebsite directory is the python package for our website.

For now the only importnat files in this directory are `settings.py`, containg
the settings for our project and `urls.py` containg our projects urls and
routing, this is how django knows that `example.com/blog/post/1/` leads to the
first blog post for example.

Django comes with a devlopment webserver. Lets start it up.

Let's go into the project root and start the webserver using the manage.py
command line utility

```
cd website
python manage.py runserver
```

We use the runserver subcommand to run the server.

This server by default runs on port 8000. Let's go to our localhost on that
port to confirm it's running.  You should see this "it works" page!

Django projects are structured as a project and apps. A project might contain
many apps, for example our website will contain a blog app but it might also in
the future contain other things we want to make. These apps can live in many
projects, so we can publish our blog app and other people can put it in there
django projects.

Let's create our blog app.

```
python manage.py startapp blog
```

This has created this directory structure

```
blog/
├── admin.py
├── apps.py
├── __init__.py
├── migrations
│   └── __init__.py
├── models.py
├── tests.py
└── views.py
```

The important files in here are

* `models.py` - These are basically your database tables, they are defined as
  python classes
* `views.py` - These take the incoming request from the user, runs some logic
  and code and returns a response

Lets start with a simple view just to confirm everything is working. Open up
views.py and add the follwowing code into it

```
from django.http import HttpResponse


def index(request):
    return HttpResponse("<h1>This is the blog index page</h1>")

```
Every view is a function, it has to take the request argument, which is the
http request from the user.

But the user has no way of getting to that view, how does django know how to
get to that view? We have to tell it with the urls.py files.

FIrst let's create a urls.py file in our blog app.

```
touch blog/urls.py
```

In this file, add the following code

*Explain this code as we are going*

```
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

This is pretty simple, we are routing any url that comes to this app with no
additonal path to the index view which we just created

We now need to point our projects root urls to our new module

in `mywebsite/urls.py` make it look like the following

```
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('blog/', include('blog.urls')),
    path('admin/', admin.site.urls),
]
```

This routes anything going to /blog/ to our blogs urls.py file.

let's start our webserver again `python manage.py runserver` and check it works
by going to `localhost:8000/blog`

We are now going to create our database, this will store our blog
posts but also things that django provides us like users and the like.

By default django uses sqlite which is fine for what we want, and to be honest
fine for most things. You can change this by editing the `settings.py` file.

run the `python manage.py migrate` command to make the database

*on vid i'm Showing it migrating and then also sqliebrowser of the tables it's created*

Now we have the base database and tables made it's time to create the ones for
our blog. 

in `blog/models.py` create the following 

```
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=150, unique=True)
    text = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
```

*explain above this in vid*

Now we need to modify our database to include these models, we need to do
2 things to do that.

First we need to tell the project root that we are using this app, so in
`settings.py` add it to the INSTALLED_APPS list

*shown in vid*

we then want to run the `python manage.py makemigrations` command, this will
tell django we want to make some changes to the database. we then make those
changes with `python manage.py migrate`

Now that we have our database set up, we should start using the admin
interface.

first we need to create our admin user

`python manage.py createsuperuser`

add appropirate information
*showin in vid*

run the webserver and navigate to `/admin/` and login.

As you can see, all we can do is modify users and groups - but that's not that
useful. Let's make it so we can edit our blogs app in the admin interface.

edit the file `blog/admin.py` and add the follwoing


```
from .models import Post
admin.site.register(Post)
```

Now go back to the admin and we can access our blogs Post model and play around
with it. Add some posts with dummy text for now.

If you look back in the blog view, the Posts don't display with there titles,
to make that so - add the following method to your Posts model in
`blog/models.py`

```
 def __str__(self):
        return self.title
```

Now refresh the admin page and you should see the posts titles instead of the
object number.

As a quick aside let's see how we can view these posts from the commandline,
using the Django ORM.

lets enter the django shell

`python manage.py shell`

we need to import our models

`from blog.models import Post`

We can then view the blog posts like so

`Post.objects.all()`

We can also filter blog posts, for example

`Post.objects.get(id=1)`
Id is a auto generated field by django.

We can also assign this to a var and look at the text

```
p = Post.objects.get(id=1)
p.text
```

Now let's create our Views. For our blog we want a few views.

* Our homepage that displays all our posts titles as clickable links
* A Post page that shows the blog in it's entirety.


Let's edit our index view to display our blog posts, using the same logic we
learnt in the shell.

```
form .models import Post

def index(request):
    posts = Post.objects.all()
    return HttpResponse("<h1> You are at the blog index page!!1! </h1>")
```
*in vid we add print statmetn to show*

We now need to display these, for this we shall take advantage of Django
templating.

Create a directry in you blog app called templates/blog/

Create a file called index.html in that, it should look like

`blog/templates/blog/index.html`

This namespaced structure allows you to refer to templates within Django as
`blog/templates`

In that template add the following code

```
<h1> Welcome to the blog </h1>
{% if posts %}
    <ul>
    {% for post in posts %}
    <li><a href="/post/{{ post.id }}/">{{ post.title }}</a></li>
    {% endfor %}
    </ul>
    {% else %}
    <p> There are no blog posts :( </p>
    {% endif %}
```

This takes provides creates a llink for each post to a url and view we have not
yet created, so let's create that.

Update the view so it looks like this

```
from django.shortcuts import render

from .models import Post

# Create your views here.

def index(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'blog/index.html', context)

```
*expalin in video, at end we remove import*

We don't need the HttpResponse import anymore. We also create a context
dictonary, this is what we pass to the template.

If you go back to your blog index page you should see the links appear.

BUt they link to nothing! it fails.

Lets edit our `blog/urls.py` file to add this url in

`path('post/<int:post_id>/', views.post, name='post')`

rember this is in our blog app so this will match something like blog/post/1

We also want to create a view that takes that post and displays it

create this view 

```
# add this import at the top of file
from django.shortcuts import get_object_or_404 

def post(request, post_id):                                                        
         post_to_display = get_object_or_404(Post, id=post_id)                          
         context = {                                                                 
             'post': post_to_display,                                                
         }                                                                           
         return render(request, 'blog/post.html', context) 
```
*explain in vid*

We also need a template for this. Make and edit the file
`blog/templates/blog/post.html`

Add the following into it

```
<h1> {{ post.title }} </h1>

<div class="post">
{{ post.text }}
</div>

<p><i>Published on {{ post.published_date }}</i></p>
```

We should also fix the link in our initial index template

```
<li><a href="/blog/post/{{ post.id }}/">{{ post.title }}</a></li>
```

Now we can view those blog posts! 

Right that's basically django, we have a really really basic but functinaing
website, we can add posts from the admin interface and they will automatically
get displyaed. 

There are many things for the future we can do here, some things are 
* Allow the writing of markdown in posts so we don't have to write html in the
  django blog
* Style the blog
* Allow adding the posts in the frontend behind a log in, this could be
  a visual WYSIWG editor
* Drafts of posts, thsi would require editing the model with a checkbox
  (boolenafield) to allow a post ot be in draft, then adding some filtering
logic to not display posts with that field checked

You can do so many things with django, go ahead and make your own project or
use this one as a launch pad, there are links in the desc to the source code.

