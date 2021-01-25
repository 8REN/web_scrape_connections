# web_scrape_connections
 ### the goal here is to search linkedin for connections, jobs, location based profiles, from search response, create dataframe with url and name of person with other details visible in minimized search format, then to iterate through urls and scrape the info from each profile, creating another csv, with all info, and create personalized message with which i can use to connect with user.
https://datainsights.data.blog/2021/01/17/web-scraping-with-selenium/
instructions on installing driver on chrome found here
can be used with other browsers, safari, opera, explorer, firefox, etc. must have matching driver for browser
selenium:
*automate login 
*navigate page buttons and pagination
*initial data scrape from search results to obtain name and url of profile
*iterate through urls 
*scrape individual profile for 
*** name
*** employment
how many jobs? fill with NaN if fewer jobs than chosen
*** education
2 colleges
*** use these columns to create a string in a new column for message to connection upon requesting to 'connect' initially
