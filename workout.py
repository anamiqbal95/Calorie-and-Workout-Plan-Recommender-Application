# Name : workout.py

## workout.py consists of WorkOut class
## the purpose of WorkOut class is to create WorkOut object that store information such as workout type, age, gender, category, and workout level
## this object will be used to store information from Main method
## and use the information to access the URL to gain information of workout informations
## and return it to main method

#importing necessary packages
import requests
from bs4 import BeautifulSoup

#defining WorkOut class
class WorkOut:

  #init method of WorkOut class
  # @param age: age from input
  # @param age: workout type from calorie intake input
  # @param age: gender from input
  def __init__(self, age, workoutType, gender):
    self.__workoutType = workoutType
    self.__age = age
    self.__gender = gender
    self.__category = ""
    self.__level = ""

  #categorizeWorkout method is used to fill in Category and Level variable
  #there are two category of workout, for adult or for seniors
  #there are three level, beginner to maintain weight, intermediate to lose weight and advanced to lose weight extremely
  def categorizeWorkOut(self):
    #workout categorized by age, if older than 50 means senior, under 50 means normal
    if self.__age >= 50:
      self.__category = "senior"
    else:
      self.__category = "normal"

    #workout type is categorized into three level, if its maintain/mild weight gain meaning beginner
    if self.__workoutType == 1 or self.__workoutType == 4:
      self.__level = "beginner"
    #if its proper weight loss/gain meaning intermediate
    elif self.__workoutType == 2 or self.__workoutType == 5:
      self.__level = "intermediate"
    #if its extreme weight loss/gain meaning advanced
    elif self.__workoutType == 3 or self.__workoutType == 6:
      self.__level = "advanced"

  #getWorkOutPlan method is to get information from the url, process it, and return necessary information
  def getWorkOutPlan(self):
    #workout information is stored in workoutList
    workoutList = []

    #this if statement is entered when the workout is for senior
    #url used due to the reasoning, people older than 50 years old is recommended to do light exercise like walking
    #not intense exercise like recommended for younger people
    if self.__category == "senior":
      url = "https://firstquotehealth.com/health-insurance-news/recommended-steps-day"

      #get information from url
      page = requests.get(url)
      soup = BeautifulSoup(page.content, 'html.parser')

      #get table
      table_body=soup.find('tbody')
      rows = table_body.find_all('tr')
      for row in rows:
        cols=row.find_all('td')
        cols=[x.text.strip() for x in cols]
        
        #find row for specific age
        if cols[0] == "65+ years old":
          #check for the workout Level, if beginner, suggest light exercise
          if self.__level == "beginner":
            for i in range (7):
              workoutList.append(["Brisk Walk", [cols[1]]])
          #check for the workout Level, if intermediate, suggest acive exercise
          elif self.__level == "intermediate":
            for i in range (7):
              workoutList.append(["Brisk Walk", [cols[2]]])
          #check for the workout Level, if advanced, suggest highly acive exercise
          elif self.__level == "advanced":
            for i in range (7):
              workoutList.append(["Brisk Walk", [cols[3]]])
      
    else:
      #this if statement is entered when the workout is not for senior
      #url specified for each gender and workout level
      url = "https://massivejoes.com/free-workout-plan/"+ self.__gender + "-" + self.__level
      
      #links are defined by gender and types of workout, this is when the gender is female
      if self.__gender == "female":
          #if type is 1-3 meaning weight loss
          if self.__workoutType <= 3:
              url = url + "-fat-loss/"
          #if type is 4-6 meaning weight gain
          else :
              url = url + "-muscle-building/"
      #if statement for when the input is male
      else:
          if self.__workoutType <= 3:
              url = url + "-fat-loss/"
          else :

                  url = url + "-build-muscle/"
            
      #get information from url
      page = requests.get(url)
      soup = BeautifulSoup(page.content, 'html.parser')
      
      #for loop is used to access each information per day
      for i in range (7):
        #get daily workout title
        currentId = "heading" + str(i+1)
        detailCurrentId = "collapse" + str(i+1)
        div = soup.find(id=currentId)
        currentTitle = div.h4.text
        splitIndex = currentTitle.find("-")
        currentTitle = currentTitle[splitIndex+2:]
        
        detaildiv = soup.find(id=detailCurrentId)
        detailString = str(detaildiv)

        #get daily workout if specified day is for resting
        if "Rest" in currentTitle:
          
          #get exercise name
          findExercise = detailString.find("EXERCISE")
          exerciseString = detailString[findExercise:]
          findworkOutName = exerciseString.find("<li>")
          findworkOutEndName = exerciseString.find("</li>")
          workoutNameString = exerciseString[findworkOutName+4:findworkOutEndName]
          
          #get duration
          findDuration = detailString.find("DURATION")
          durationString = detailString[findDuration:]
          finddurationName = durationString.find("<li>")
          finddurationEndName = durationString.find("</li>")
          durationNameString = durationString[finddurationName+4:finddurationEndName]
          
          #store it to workoutList
          currentExercise = [currentTitle, [(workoutNameString + " - " + durationNameString)]]
          workoutList.append(currentExercise)
        
        #get daily workout if specified day is for exercise
        else:
          #find index of each information
          findExercise = detailString.find("EXERCISE")
          findReps = detailString.find("REPS")
          findSets = detailString.find("SETS")

          #process information about daily exercise detail which is the exercise name
          #once information is gathered, information is stored into list exerciseList
          exerciseString = detailString[findExercise+19:findReps]
          findExerciseEnd = exerciseString.find("</ul>")
          exerciseString = exerciseString[:findExerciseEnd-1]
          exerciseString = exerciseString.replace("<li>", "")
          exerciseString = exerciseString.replace("\n", "")
          exerciseString = exerciseString.replace("</li>", ",")
          exerciseString = exerciseString[:-1]
          exerciseList = exerciseString.split(',')

          #process information about daily exercise detail which is the reps to be done for each exercise
          #once information is gathered, information is stored into list repsList
          repsString = detailString[findReps+15:findSets]
          findRepsEnd = repsString.find("</ul>")
          repsString = repsString[:findRepsEnd-1]
          repsString = repsString.replace("<li>", "")
          repsString = repsString.replace("\n", "")
          repsString = repsString.replace("</li>", ",")
          repsString = repsString[:-1]
          repsList = repsString.split(',')

          #process information about daily exercise detail which is how many sets to be done for each exercise
          #once information is gathered, information is stored into list setsList
          setsString = detailString[findSets+15:]
          findSetsEnd = setsString.find("</ul>")
          setsString = setsString[:findSetsEnd-1]
          setsString = setsString.replace("<li>", "")
          setsString = setsString.replace("\n", "")
          setsString = setsString.replace("</li>", ",")
          setsString = setsString[:-1]
          setsList = setsString.split(',')
          
          allExercise = []
          #store each row of information in allExercise list
          #each row will consist of a string that reflects what exercise to be done and how many reps and sets to be done
          for j in range(len(exerciseList)):
            allExercise.append(exerciseList[j] + " - " + repsList[j] + " Reps " + setsList[j] + " Sets")
          
          #store information into workoutList
          currentExercise = [currentTitle, allExercise]
          workoutList.append(currentExercise)

    #return the complete weekly workoutList
    return workoutList