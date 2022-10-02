# Blogin

Blogin is a personal blog website that base on flask development.

## Introduce

The personal blog site developed by the Flask Python Web framework consists of two parts: the front-end and the back-end.

### Front-end

1. **Personal Blog**
   - Support blog categorization
   - Support comment 
   - Support  share your blog to personal social network
   - Support blog archive
2. **Personal Gallery**
   - Support photo tag
   - Support comment and like
   - Support share your photo to personal social network
3. **Online Lite Tool**
   - Online word cloud graph generator
   - Online multi translation tool
   - Online Tang-Song poem search tool
   - Online ocr tool
   - Online IP real address search tool
4. **Comment System**
   - Support comment/delete/report
   - Support reply comment
5. **Personal Profile**
   - Personal profile card
   - Message notifycation
   - Modify your information
   - Record login log
6. **Others**
   - Support make personal plan recently
   - Support the contribution heat map display for the past three months

### Back-end

1. **Content manage**

   - **Blog** 
     - Create blog
     - Modify blog
     - Delete blog(It's just masking the display on the front page, not actually deleting it from the database)
   - **Gallery**
     - Add photo
     - Modify Photo
     - Delete Photo(like blog)
   - **Personal Plan**
     - Add a new personal plan
     - Modify personla plan
     - Finish personal plan

2. **Social Mange**

   - **Comment Manage**
     - Look up comments
     - Delete comment(like blog)
   - **User Manage**
     - Look up users
     - Ban user account

3. **Server Manage**

   - **Server Satus**
     - CPU Usage
     - Memory Usage
     - Network Status

   - **Log**
     - App Log

4. **Others**

   - **Friend Link**
     - Add new friend link
     - Abandon a friend link
   - **Milestone**
     - Add new milestone
     - Abandon a milestone

## Start

### Dependencies

1. **Install mysql**

2. **Install redis**
   
3. **Create Database**

### Initial

1. **Configure environment variables** 

   ```INI
   MAIL_SERVER='your mail server'
   MAIL_USERNAME='your mail username'
   MAIL_PASSWORD='your mail server verify code' # not your email login password
   SECRET_KEY='your project secret'
   DATABASE_USER='your database connect username'
   DATABASE_PWD='your database connect user password'
   ```

2. **Init database**

   Enter the root directory of the project, use the following command to initialize the database.

   ```shell
   cd Blogin
   flask admin
   ```

3. **Run**

   ```shell
   flask run
   ```