
# Name : 
    #calorie.py
# Purpose: 
    #This class takes user input on variables such as age, gender, height, weight, activity level
    #and allows us to use these inputs to call an API
    #and get information on 1) user BMI and 2) calorie intake requirements
    #This class also calculates a benchmkarked BMI using a csv file with 500+ rows 
    #on physically active individuals
    #This benchmarked BMI is compared with the user current BMI and suggestions are made
    #to help the user make a more informed decision on what goal they should set
## calorie.py

#JSON is a lightweight format for storing and transporting data
#JSON is often used when data is sent from a server to a web page
import json
import math
import requests
import pandas as pd

class Calorie:
  '''
  Class to fetch and calculate Calorie and BMI.
  '''

  # Initializing all variables.
  def __init__(self, userInput):   
    self.input_dictionary = userInput           #Dictionary to store user input
    self.bmi = 0.0                              #Variable to store BMI from API.
    self.calorie_intake_requirements = {}       #Dictionary to store different calorie requirements based on the goal.
    self.ref_data = pd.read_csv("src/Body_measurements_of_507_physically_active_individuals.csv")    #Reference data.
    self.mean_age_and_gender_bmi = 0.0        #Variable to store mean age and gender bmi from reference data.
    self.required_calories = 0                #Variable to store final required calories.

  # API link for putting user input and getting user output on BMI and Calorie Intake Requirements
  #https://rapidapi.com/malaaddincelik/api/fitness-calculator/

  #2: 
  #This function gets the BMI from the API link based on user inputs.
  def getBMIFromAPI(self):
      #print(self.input_dictionary)
      url = "https://fitness-calculator.p.rapidapi.com/bmi"

      #put that inputDictionary in API link for website for BMI:
      querystring = {
                     "age": str(round(self.input_dictionary['age'])) ,
                     "weight":str(self.input_dictionary['weight']),
                     "height":str(self.input_dictionary['height'])
                     }

      headers = {
          'x-rapidapi-host': "fitness-calculator.p.rapidapi.com",
          'x-rapidapi-key': "b0e38d457amshf93059959318267p152217jsn57a509da2f2d"
          }

      response = requests.request("GET", url, headers=headers, params=querystring)

      # json.loads converts string json response.text into a python object that we can use in the code 
      responseDict = json.loads(response.text)
      BMI = responseDict['data']['bmi']

      self.bmi = BMI

      return self.bmi

  #3:
  ##benchmarked BMI from CSV file (one time calculation)
  # Function to calculate the mean bmi from the referance bmi based on the age and gender of the user.
  # This method checks if there are entries for the user-entered age and genders, if it exists, then it calculates the mean bmi based on the formula,
  # BMI  = (Weight/(Height*100)^2) 
  # If no entries are found for the user-entered age and genders, the mean bmi is calculated for all rows belonging to the range of (age-5,age+5)
  def calculateBenchmarkedBMI(self):
      #Dictionary to convert user input to ref data key for sex/gender.
      gender_dict = {"male": 1, "female": 0}
      
      #Filtering data based on age and gender entered by the user.
      filtered_df = self.ref_data[(self.ref_data['age'] == self.input_dictionary['age']) 
                              & (self.ref_data['sex'] == gender_dict[self.input_dictionary['gender']])]

      #If user-entered values are not found, then take all rows belonging to the range(age-5,age+5)
      if len(filtered_df)==0:
        filtered_df = self.ref_data[((self.ref_data['age']>self.input_dictionary['age']-5)
                                 & (self.ref_data['age']<self.input_dictionary['age']+5)) 
                                 & (self.ref_data['sex'] == gender_dict[self.input_dictionary['gender']])]

      #Function to calculate square.
      def square(x):
        return math.pow(x,2)

      #Calculating bmi for all rows in the filtered df.(We divide height by 100 here to convert from centimeters to meters.)
      bmi_series = filtered_df['wgt']/(filtered_df['hgt']/100).apply(lambda x: square(x))

      self.mean_age_and_gender_bmi = bmi_series.mean()

      return self.mean_age_and_gender_bmi

  #4:
  #compare user BMI from API to benchmarked BMI from csv
  def interpretBMI(self):
      bmi = self.input_dictionary['weight']/math.pow(self.input_dictionary['height']/100,2)
      diff_in_bmi = bmi - self.calculateBenchmarkedBMI()
      
      print("Difference in your BMI and Benchmarked BMI: " + str(round(diff_in_bmi, 2)))
      
      # giving user different suggestions on their goals depending on 
      #whether the difference in their BMI and benchmarked BMI is
      # positive, negative or zero
      if(diff_in_bmi > 0):
          print('Based on the above difference, we suggest you take up goals that help you reduce weight to reach your ideal BMI')
      elif(diff_in_bmi <0):
          print('Based on the above difference, we suggest you take up goals that help you gain weight to reach your ideal BMI')
      else:
          ("Based on the above difference, we suggest you take up goals that help you maintain weight to stay at your ideal BMI")
          
      return round(diff_in_bmi,2)

  #5:
  #Getting calorie requirements from the API link
  #This will be used to make the meal plan and workout plan
  def getCalorieIntakeRequirementsFromAPI(self):
      url = "https://fitness-calculator.p.rapidapi.com/dailycalorie"

      #put that inputDictionary in API link for website for Calorie intake requirements:
      querystring = {
                     "age": str(round(self.input_dictionary['age'])) ,
                     "weight":str(self.input_dictionary['weight']),
                     "height":str(self.input_dictionary['height']),
                     "gender":str(self.input_dictionary['gender']),
                     "activitylevel":"level_" + str(self.input_dictionary['activity'])
                     }

      headers = {
          'x-rapidapi-host': "fitness-calculator.p.rapidapi.com",
          'x-rapidapi-key': "b0e38d457amshf93059959318267p152217jsn57a509da2f2d"
          }

      response = requests.request("GET", url, headers=headers, params=querystring)

      #print(response.text)
      # return 1. weight loss choices
      # return 2. calorie  requirement daily bmr

      responseDict = json.loads(response.text)
      self.calorie_intake_requirements = responseDict["data"]

      return self.calorie_intake_requirements

  #6:
  #give user options on the weight loss options
  #and eventually use this for output = ideal calories for meal plan and work out plan
  def decisionOnWeightLossOption(self):
      print("Provided is option of goals you might want to achieve:")
      print("1: Maintain Weight")
      print("2: Weight loss")
      print("3: Extreme weight loss")
      print("4: Mild weight gain")
      print("5: Weight gain")
      print("6: Extreme weight gain")

      user_decision = int(input("Please pick your goal:"))

      while True:
        try:
          if (user_decision == 1):
              self.required_calories = self.calorie_intake_requirements["goals"]["Mild weight loss"]["calory"]
              break
          elif (user_decision == 2):
              self.required_calories = self.calorie_intake_requirements["goals"]["Weight loss"]["calory"]
              break
          elif (user_decision == 3):
              self.required_calories = self.calorie_intake_requirements["goals"]["Extreme weight loss"]["calory"]
              break
          elif (user_decision == 4):
              self.required_calories = self.calorie_intake_requirements["goals"]["Mild weight gain"]["calory"]
              break
          elif (user_decision == 5):
              self.required_calories = self.calorie_intake_requirements["goals"]["Weight gain"]["calory"]
              break
          elif (user_decision == 6):
              self.required_calories = self.calorie_intake_requirements["goals"]["Extreme weight gain"]["calory"]
              break
          else:
              print(">>Wrong input: Please enter correct choice!")
        except ValueError:
          print(">> Wrong input, goal choice should be a number!")
          continue
  
      return {'option':user_decision, 'calorie_requirement': self.required_calories}
  