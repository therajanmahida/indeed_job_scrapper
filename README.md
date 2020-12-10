# BIA660 Final Project
indeed.com scraper and job type predictor
Here is a tutorial on how to run, and what each file does.

## Part 1: Scraper
The first file to run is the web scraper. The scraper takes as input a URL to the first page of the job listings to a particular job and returns a csv of the text descriptions of each job, and the job type, spearated by comma.

The basic steps of the scraper are:
1. open the html containing the list of jobs
2. get the 'a' tag for each job from the list of jobs
3. open the url for each a tag (for each job).
4. save the html for the job site into disc
5. get the job text for each job_html and add it to a row in the csv

The lines on the scraper are extensively commented, so please open the file to see detailed info on what each line is doing.

To run, input the URL, the number of pages you'd like to examine (there are 15 jobs per page), and the job type (one of: data enginner, data scientist, software engineer)

for example: 
run_scraper("https://www.indeed.com/jobs?q=Data+Engineer&l=Washington%2C+DC&radius=100", 2, "data engineer")
will get the first 30 jobs for data engineer in washington DC

## Part 2: Preprocessing data
The second file includes splitting, shuffling and vectorizing the data stored in the CSV file. This script will save the vectorize data to disk so we only have to run this once. 
1. Load the data to dataframes, column B of the csv containing the job type is loaded into dataframe all_y and column A containing the text of the job is loaded into all_X
2. To make the problem less trivial, the obvious clues to the job type are removed. Obvious clues are the actual job type names and their derivations.
3. Use an off the shelf function to Divide the data into training sets and testing sets 
4. Vectorize the data sets - to change the strings into numerical data. 
5. Save the vectorized training and testing data and labels to memory, so we don't have to run this file again.

## Part 3: Perform Grid Search to find best model
The third file uses SKlearn's grid search over six different models with many combinations of parameters in order to find the best model. This search is very computationally expensive, and it only needs to run once. The file performs the following tasks:
1. loading the data to apply different classifiers to perform grid search
2. Classifiers such as KNN, Decision Tree, MLP, SVC, Logistic Regression, Naive Bayes are used
3. All these classifiers are used to get the best possible accuracy

## Part 4: Voting Classifier
After running grid search we have a good idea of which models perform best for this task, as well as the top performing hyper-parameters. The voting classifier trains an ensemble predictor using the top performing individual models.
1. The user enters the models with their top performing hyperparameters. We use the top 3 performing models.
2. The Voting classifier instance is created using the models we chose.
3. The accuracy of the voting classifier is printed, as well as a confusion matrix.
    
# How to run?
1. Edit the the part1 script with the URL and job type (lines 110+) as indicated above. It will create a CSV and an alreadyseen.txt file that will prevent repeats.
2. When you are done scraping and you are satisfied with the number of jobs you got, simply run the part2 script as is. *No inputs are needed on part 2 script.*
3. Run the part3 script as is, or if you have a clue on the models and/or hyperparameters that you think are worth trying, you can run it with those alone to save computation time. If you have no clue on what would work, simply run it as is and cover all your bases. *No inputs are needed on part 3 script*. I recommend you take note of the outputs of this file, since you dont want to have to run it again, its very slow.
4. Open part4 script and enter the hyperparametes that you found on the output of part3 on lines 27-33. Choose which of those models you want to use to predict, and build a predictors list similar to the ones on lines 36-37. Run the code to obtain an accuracy and confusion matrix.
