# Week 4 — Competency reflection

## Competency claim

**C4 — APIs and Data Acquisition**

## My response:
This assignment helped me understand how APIs actually work beyond just copying a URL into Python. I used the REST Countries API, and my script pulls country data like names, regions, populations, languages, currencies, and time zones, then saves it into a CSV file. The REST Countries API didn't require a key, so I didn't need to create a .env file for this project. The part I did run into issues with was figuring out the fields parameter, because the /all endpoint in my API URL wasn't returning data, and I later learned how to specify the fields I wanted back.

As I mentioned, one thing I got stuck on was thinking the API URL by itself would just return all the data, but then when I opened it I got an error saying {"message":"'fields' query not specified or you're requesting more than 10 fields","status":400}. I used Cursor to help explain the reason and that's what helped me realize the URL was only part of the request and that I also needed parameters, which I've since learned are the extra instructions that tell the API what fields I actually want back. So, the parameters I chose were "name,cca2,region,subregion,population,languages,currencies, and timezones." Then, with Cursor's help, I added the PARAMS section so the script asks for specific fields instead of everything at once. This made the API process make more sense to me and I now understand the endpoint is where I’m asking for data, the parameters then narrowed down my request and the JSON response is what Python can organize into a readable CSV file.








