# A Model for Investing in Movies  
Movie business is notorious for being unpredictable in terms of profitability. As such, I decided to create a predictive model that would allow to more accurately estimate how much any given motion picture project would make.
## Premise  
You are a potential investor into a movie project. You need to find the best kind of project to invest in. I need to find the best indicators that any given movie project may succeed financially. The body of this text is going to be fairly high level, but technical details are available in appendices.
## Strategy  
I used a Python web scraping package BeautifulSoup to obtain data from boxofficemojo.com (and later supplemented a lot of missing budget data from the-numbers.com). I then used Python’s Pandas data analysis library to clean up the data, add missing budget data from the additional data set, and remove the rest of the missing data points. Finally, I implemented statsmodels and sklearn Python packages to select best features based on suitable correlation with domestic gross and on the p-value based relevance to the model, to create the model, re-evaluate, and improve it.
## Data Trouble  
My code tried accessing over 14,000 movie pages to obtain such data as movie title, movie rank, studio, genre, runtime, budget, MPAA rating, directors, actors, writers, producers, composers, gross, release date, etc. The movie release years were supposed to be from 1980 and up until now. However, when I looked at the resultant data set, only about 9,000 pages actually yielded some information with dates starting from 2002. Furthermore, when I cleaned it up, removed some irrelevant or bad columns and rows, and collated it with another data set, only about 3,000 data points were available for modeling. It is a huge decrease from the original number, but, as you will see, the model had no problem using this shrunk data set to predict domestic gross of movies.
At first, I had an idea to work with individuals' names and even groups of individuals. However, this would create too many indicators. Additionally, my web scraper did not do so well with groups of names (such as movie cast) and mostly yielded empty lists. Therefore, I decided to drop names as variables in predicting domestic movie gross in favor of a more general descriptor of gender:
only gender of a top participant in each category (director, writer, actor, producer, and composer) was considered.  
## Intermediate results  
As I was going through and arranging my data for eventual model building, I stumbled upon some interesting findings. For a more obvious example, more movies are released around winter holiday season:  
![Movie count based on release month](http://i.imgur.com/ilUFeKK.png)  
A little bit more surprising was to see huge participation discrepancies in gender. I used [gender-guesser Python package](https://pypi.python.org/pypi/gender-guesser/) which helped me obtain people's gender based on their first name. Where I wasn't able to pull a person's name, it would guess "unknown". Where the name could belong to either gender, it would guess "andy", but I assigned any such person to the unknown category to keep things simple. In addition, some persons had "mostly_male" or "mostly_female" names, so I made a decision to assign them to "male" and "female" categories, respectively. After processing people's names this way I discovered that females were a minority in every movie genre, every MPAA rating, and every role. Here is an example for gender participation among directors in movies based on MPAA rating:  
![Gender participation among directors based on MPAA rating](http://i.imgur.com/3SUPtXH.png)  
## Final Model Results  
After all was said and done, my model seemed to perform fairly well at guessing how much any given project would make. The model was capable of explaining ~73% of the variation in gross (R-squared value = 0.73):
![Domestic Gross of a Movie, Prediction vs. Reality](http://i.imgur.com/U7gE791.png)  
In more concrete terms:
* For every $2.45 spent on budget, domestic gross of a movie should increase by $4.24.
* Employing a small studio should decrease domestic gross of a movie by $7621
* For every day a movie stays in theaters, the domestic gross should increase by /$1.39.
* etc., see more details below:  
![Coefficients Table](http://i.imgur.com/EHiuYSv.png)  
Side note on budget's impact on domestic gross: both sets underwent Box-Cox transformation to be more normal. Therefore, to examine budget impact on domestic gross, we can convert ~1.7 to real dollars ($4.24) to understand what 1 transformed unit of budget does. Now, if we convert 1 unit of budget back to real world units, we will get $2.45. Lambdas used for transformation were 0.22252031174182518 for domestic gross and 0.24082885387145095 for budget. I used the formula found on [SO](https://stackoverflow.com/questions/26391454/reverse-box-cox-transformation) to perform my conversions. The formula along with the code are the following:  
```python
def invboxcox(y,ld):
   if ld == 0:
      return(np.exp(y))
   else:
      return(np.exp(np.log(ld*y+1)/ld))
```

<iframe src="https://docs.google.com/presentation/d/15nYh2ICHJ9ZoVk-m5DHrCMui4yDV3N7i2V4mADXclHw/embed?start=false&loop=false&delayms=3000" frameborder="0" width="960" height="569" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>
