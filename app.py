
from datetime import datetime
from distutils.command.upload import upload
from email.policy import default
from fileinput import filename
from operator import ipow
import re
import secrets
from sqlite3 import Cursor
from turtle import title
from types import MethodDescriptorType
from wsgiref.validate import validator
from flask import Flask , render_template, url_for,request,redirect, session ,flash,jsonify
from datetime import datetime
from flask_mysqldb import MySQL
import os
import secrets

app = Flask(__name__)
#secret key
app.config['SECRET_KEY'] = "qwerty123" 


#database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bloglogin.sqlite3'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'batfast'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mysql = MySQL(app)


def convert_blog_image(blogImage):
        hash_image = secrets.token_urlsafe(10)
        _, file_ext = os.path.splitext(blogImage.filename)
        img_name = hash_image + file_ext
        file_path = os.path.join(UPLOAD_FOLDER,img_name)
        blogImage.save(file_path)
        return img_name

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")




@app.route("/get-touch", methods = ['GET','POST'])
def get_touch():
        if request.method == 'POST':
                getName = request.form['getName']
                getEmail = request.form['getEmail']
                getMsg = request.form['getMsg']
                cursor = mysql.connection.cursor()
                cursor.execute("INSERT INTO gettouch (getName,getEmail,getMsg) VALUES(%s,%s,%s)",(getName,getEmail,getMsg))
                mysql.connection.commit()
                cursor.close()
                gtSucess = jsonify({'getName':getName})
                return  gtSucess



@app.route("/blog-login" , methods =['GET','POST'])
def blog_login():
        if request.method == 'POST':
                userName = request.form['name']
                emailId = request.form['email']
                if not userName or not emailId:
                        flash('Please enter all the fields', 'error1')
                elif  userName != "test" or  emailId != "test123":
                        flash('Please enter the correct account Details', 'error2')
                else:
                        session["userName"] = userName
                        return redirect(url_for("blog_content"))
        else:
                return render_template("blog-login.html")


@app.route("/blog-content",methods =['GET','POST'])
def blog_content():
        if "userName" in session:                    
                if request.method == "POST":
                        blogTitle = request.form['bTitle']
                        blogContent = request.form['bContent']
                        blogImage = convert_blog_image(request.files.get('bImage'))
                        
                        if not blogTitle or not blogContent:
                                flash('Atleast enter Blog title and Blog Content', 'Blog_error')   
                        else:
                                cursor = mysql.connection.cursor()
                                cursor.execute("INSERT INTO  blogcontent  (title,content,image) VALUES(%s,%s,%s)",(blogTitle,blogContent,blogImage))
                                mysql.connection.commit()
                                cursor.close()
                                return redirect(url_for("blogs"))
        else:
                return redirect(url_for("blog_login"))
        return render_template("blog-content.html")

@app.route("/blogs", methods = ['GET','POST'])
def blogs():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM blogcontent ORDER by id")
        blogFetch = cursor.fetchall()
        return render_template("blog.html" , blogres = blogFetch)


@app.route("/view-blog/<int:id>")
def view_blog(id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM blogcontent WHERE id = %s",(id,))
        blogFetch = cursor.fetchall()
        return render_template("view-blog.html",blogFetch = blogFetch)

@app.route("/blog-management", methods = ['GET','POST'])
def blog_management():
        if "userName" in session: 
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT * FROM blogcontent ORDER by id")
                blogFetch = cursor.fetchall()
                return render_template ("blog-management.html" ,blogFetch = blogFetch)
        else:
                return redirect(url_for("blog_login"))

@app.route("/update-blog",methods = ['GET','POST'])
def update_blog():
        if request.method == 'POST':
                blogId = request.form.get('blogId')
                blogTitle = request.form['blogTitle']
                blogContent = request.form['blogContent']
                cursor = mysql.connection.cursor()
                cursor.execute("""UPDATE blogcontent SET title = %s, content = %s  WHERE id = %s""",(blogTitle,blogContent,blogId,) )
                mysql.connection.commit()
                cursor.close()
                upData = jsonify({'blogId':blogId,'blogTitle':blogTitle,'blogContent':blogContent})
                return  upData


@app.route("/delete-blog",methods= ['GET','POST'])
def delete_blog():
        if request.method == 'POST':
                deblogId = request.form.get('deblogId')
                cursor = mysql.connection.cursor()
                cursor.execute("""DELETE FROM blogcontent  WHERE id = %s""", (deblogId,))
                mysql.connection.commit()
                cursor.close()
                retData = jsonify({'deblogId':deblogId})
                return retData

@app.route("/image-update",methods= ['GET','POST'])
def image_update():
        if request.method == 'POST':
                blogImage = convert_blog_image(request.files.get('bImage'))
                bId = request.form.get('bId')
                cursor = mysql.connection.cursor()
                cursor.execute("""UPDATE blogcontent SET image = %s  WHERE id = %s""",(blogImage,bId,) )
                mysql.connection.commit()
                cursor.close()
                return redirect(url_for('blog_management'))

if __name__ == '__main__':
   app.run(host='localhost', port=5000)
   app.run(debug = True)

