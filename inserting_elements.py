#!/usr/bin/python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Users, Programs, Courses, Base
from sqlalchemy_utils import database_exists, drop_database, create_database


engine = create_engine('sqlite:///udacity_courses.db')

# Dropping existing elements from database and recreate a new schema
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Linking the metadata of the Base class to our engine 
# so that the declaratives can be accessed 
# using a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# Creating one user user at least
# so we can insert programs and courses

user = Users(name='SID ALI MAHMOUDI', email='fs_mahmoudi@edu.esi.dz',
             picture='https://bit.ly/2JpvAGI')
session.add(user)
session.commit()

# Inserting some programs items
# The user_id is by default 1

program1 = Programs(title='Artificial Intelligence')
session.add(program1)
session.commit()

program2 = Programs(title='Data Science')
session.add(program2)
session.commit()

program3 = Programs(title='Cloud Computing')
session.add(program3)
session.commit()

program4 = Programs(title='Programming and Development')
session.add(program4)
session.commit()

program5 = Programs(title='Autonomous Systems')
session.add(program5)
session.commit()

program6 = Programs(title='Business')
session.add(program6)
session.commit()


# Inserting some courses in each program
# The user_id is by default 1

course = Courses(title='Machine Learning Engineer',
                 description='''Learn advanced machine learning algorithms 
                 and how to deploy your models to a production environment.
                 Gain practical experience using Amazon SageMaker to deploy
                 trained models to a web application and evaluate its performance.
                 AB test models and learn how to update the models as you gather more data.''',
                 programs=program1,
                 )
session.add(course)
session.commit()

course = Courses(title='Deep Learning',
                 description='''Deep learning is driving advances in artificial
                 intelligence that are changing our world. Enroll now to build
                 and apply your own deep neural networks to challenges like image
                 classification and generation, time-series prediction, and model deployment.''',
                 programs=program1,
                 )
session.add(course)
session.commit()

course = Courses(title='Natural Language Processing',
                 description='''Master the skills to get computers to understand,
                 process, and manipulate human language. Build models on real data,
                 and get hands-on experience with sentiment analysis,
                 machine translation, and more.''',
                 programs=program1,
                 )
session.add(course)
session.commit()

course = Courses(title='Data Scientist',
                 description='''Gain real-world data science experience with projects
                 designed by industry experts. Build your portfolio and advance
                 your data science career.''',
                 programs=program2,
                 )
session.add(course)
session.commit()

course = Courses(title='Data Engineer',
                 description='''Data Engineering is the foundation for the new world of
                 Big Data. Enroll now to build production-ready data infrastructure,
                 an essential skill for advancing your data career.''',
                 programs=program2,
                 )
session.add(course)
session.commit()

course = Courses(title='Predictive Analytics for Business',
                 description='''Learn to apply predictive analytics and
                 business intelligence to solve real-world business problems''',
                 programs=program2,
                 )
session.add(course)
session.commit()

course = Courses(title='Cloud Developer',
                 description='''Cloud development is the foundation for the new world
                 of software development. Enroll now to build and deploy
                 production-ready full stack apps at scale on AWS,
                 an essential skill for advancing your web development career.''',
                 programs=program3,
                 )
session.add(course)
session.commit()

course = Courses(title='Cloud Dev Ops Engineer',
                 description='''Companies are looking for talented DevOps engineersto remain
                 competitive in this agile world. Enroll now to operationalize infrastructure
                 at scale and deliver applications and services at high velocity,
                 an essential skill for advancing your career.''',
                 programs=program3,
                 )
session.add(course)
session.commit()

course = Courses(title='C++ Developer',
                 description='''Learn C++, a high-performance programming language used in
                 the world's most exciting engineering jobs -- from self-driving cars and
                 robotics, to web browsers, media platforms, servers, and even video games.''',
                 programs=program4,
                 )
session.add(course)
session.commit()

course = Courses(title='Full Stack Developer',
                 description='''In this program, you’ll prepare for a job as a Full Stack
                 Web Developer, and learn to create complex server-side web applications
                 that use powerful relational databases to persistently store data.''',
                 programs=program4,
                 )
session.add(course)
session.commit()

course = Courses(title='Blockchain Developer',
                 description='''Demand for blockchain developers is skyrocketing.
                 In this program, you'll work with the Bitcoin and Ethereum protocols,
                 build projects for real-world application, and gain the essential
                 skills for a career in this dynamic space.''',
                 programs=program4,
                 )
session.add(course)
session.commit()

course = Courses(title='Robotics Software Engineer',
                 description='''Build hands-on projects to acquire core robotics
                 software engineering skills: ROS, Gazebo, Localization, Mapping,
                 SLAM, Navigation, and Path Planning.''',
                 programs=program5,
                 )
session.add(course)
session.commit()

course = Courses(title='Self Driving Car Engineer',
                 description='''Self-driving cars are transformational technology,
                 on the cutting-edge of robotics, machine learning, and engineering.
                 Learn the skills and techniques used by self-driving car teams at
                 the most advanced technology companies in the world.''',
                 programs=program5,
                 )
session.add(course)
session.commit()

course = Courses(title='Business Analytics',
                 description='''Gain foundational data skills applicable to any industry.
                 Collect and analyze data, model business scenarios, and communicate your
                 findings with SQL, Excel, and Tableau.''',
                 programs=program6,
                 )
session.add(course)
session.commit()

course = Courses(title='Predictive Analytics for Business',
                 description='''Learn to apply predictive analytics and
                 business intelligence to solve real-world business problems''',
                 programs=program6,
                 )
session.add(course)
session.commit()

course = Courses(title='Digital Marketing',
                 description='''Gain real-world experience running live campaigns as you 
                 learn from top experts in the field. Launch your career with a
                 360-degree understanding of digital marketing.''',
                 programs=program6,
                 )
session.add(course)
session.commit()

print('\nInserting all elements was successful!')
