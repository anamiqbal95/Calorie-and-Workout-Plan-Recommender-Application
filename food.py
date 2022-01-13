# Name : food.py

# Purpose: It allows to get a dictionary with the meal plan per day from https://www.prospre.io/meal-plans/
# The class uses the calorie intake based on the user selection
# and retrieves the information from the appropiate weblink
# the information is structured with the support of dictionaries and lists
# the program returns a dictionary, which gathers the meal plan per day

# imports required for webscrapping
import requests
from bs4 import BeautifulSoup

class FoodRecommendation:
    

    # Constructor
    # It receives the calorie intake based on the election of the user
    # @param recommendedCal
    #
    
    def __init__(self, recommendedCal):
        self.__calories = recommendedCal
        self.__closestCal = 0
    
    # This method receives the calorie intake based on the election of the user
    # Gets the meal plan from "https://www.prospre.io/meal-plans/"
    # Returns a dictionary with a meal plan for each day of the week
    # @return dictionary dayDict
    #/
    def getRecommendation(self):
        
        # The website "https://www.prospre.io/meal-plans/" has many links: 1000 calories, 1100 calories, 1200 calories until 3400
        # The code lines round the calorie intake from the user to one of the fixed calories the website has
        
        self.__closestCal =round(self.__calories/100)*100
        mealBasicInfoDict=dict()
        dayDict=dict()
        macroList=list()
        
        
        minCalories=1000
        maxCalories=4000
        calorieCorrection=1300
        
        #Since the website only provides meal plan for [1000,4000] calories
        #A min and max values are setted to retrieve the information
        
        if self.__closestCal<minCalories:
            self.__closestCal=minCalories
        if self.__closestCal>maxCalories:
            self.__closestCal=maxCalories

        # The website has a small difference in the link for 1300 calories
        # So the if condition allows to handle it
        
        if self.__closestCal==calorieCorrection:
            link="https://www.prospre.io/meal-plans/"+str(self.__closestCal)+"-calories-meal-plan"
        else:
            link="https://www.prospre.io/meal-plans/"+str(self.__closestCal)+"-calorie-meal-plan"
            
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser') 
        typeList = ['Calories', 'Protein', 'Fat', 'Carbohydrates']
        
        #Since the structure of the website is not grouped by day
        #a list is gathering all nutrients and macros
        
        nutrientDay=soup.find_all("div", {"class": "nutrient-summary"})
        for a in nutrientDay:	
            amount=a.find_all(class_="macro-amount")
            for b in amount:
                macroList.append(b.get_text())

        d=1
        
        #The list of macros is grouped by day
        #and each group is stored in dayDict
        
        for i in range(0,len(macroList),+4):
            mealBasicInfoDict=dict()
            dayDictComponent=list()
            value=macroList[i:i+4]
            basicInfoDict=dict(zip(typeList, value))
            mealBasicInfoDict['MealBasicInfo']=basicInfoDict
            dayDictComponent.append(mealBasicInfoDict)
            tagDay="Day"+str(d)
            dayDict[tagDay]=dayDictComponent
            d=d+1
      
        #The code retrieves the information of each meal type (breakfast, main, snack)
        #the components of the meal and the quantity of each one
        
        meal = soup.find_all('div', {"class": "meal-card"})
        foodList = list()
        for m in meal:
            mealRecipesDict=dict()
            mealTypeDict=dict()
            h3 = m.find('h3')
            mealComponent = h3.get_text()
            mealComponentQuantity= mealComponent.split(':')[1].strip()
            mealComponentName= mealComponent.split(':')[0].strip()
            detail=m.find_all('div',{"class":"meal-columns w-row"})
            recipesList=list()
            for d in detail:
                recipeDict=dict()
                name=d.find(class_="recipe-name").get_text()
                amount=d.find(class_="recipe-amount").get_text()
                recipeDict[name]=amount
                recipesList.append(recipeDict)
            mealRecipesDict[mealComponentQuantity]=recipesList
            mealTypeDict[mealComponentName]=mealRecipesDict
            foodList.append(mealTypeDict)

        
        #Divides the foodList in groups considering that days can have different meal types
        #The codes divides the list looking if the meal type=breskfast
        #then it means a new group is initialized with a new day.
        #stores the meals  in dayDict
        d=0
        for i in range (0, len(foodList)):
            if 'Breakfast' in foodList[i].keys():
                d=d+1
                tagDay="Day"+str(d)
                dayDict[tagDay].append(foodList[i])   
            else:   
                dayDict[tagDay].append(foodList[i])   
                
        return dayDict