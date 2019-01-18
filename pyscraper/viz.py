import tldextract
import pandas as pd
import json
import os
import bs4

def structure_url(page_urls):

    # Extract Domain
    tldeext = tldextract.extract(page_urls[0])
    domain = '.'.join(tldeext)

    # Structure page URLS
    page_urls = [url.split(domain)[1:][0] for url in page_urls]

    return page_urls, domain

def parent_to_child_url(page_urls):

    category = [] ; sub_category = [] ; sub_category_type = []

    # Get parent to child of URLs
    for url in page_urls:
        data = list(filter(None, url.split('/')))
        for i,k,j in zip(data[0::1], data[1::1], data[1::2]):
            category.append(i)
            sub_category.append(k)
            sub_category_type.append(j)

    # Seperate to prepare for dataframe to flare format for D3.js
    df = pd.DataFrame({'category': category,'sub_category': sub_category,'sub_category_type':sub_category_type})
    df = df.groupby(['category','sub_category','sub_category_type']).size().reset_index()
    df.rename(columns={0: 'count'}, inplace=True)

    return df

def dataframe_to_flare(df,page_urls,domain):

    # order in the groupby here matters, it determines the json nesting
    # the groupby call makes a pandas series by grouping "category", "sub_category" and"sub_category_type",
    #while summing the numerical column 'count'

    df1 = df.groupby(["category", "sub_category","sub_category_type"])['count'].sum()
    df1 = df1.reset_index()

    # Transform into Flare.json
    d = {"name":domain, "children": []}

    for line in df1.values:
        category = line[0]
        sub_category = line[1]
        sub_category_type = line[2]
        count = line[3]

        # make a list of keys
        category_list = []
        for item in d['children']:
            category_list.append(item['name'])

        # if 'category' is NOT category_list, append it
        if not category in category_list:
            d['children'].append({"name":category, "children":[{"name":sub_category, "children":[{"name": sub_category_type, "size" : count}]}]})

        # if 'category' IS in category_list, add a new child to it
        else:
            sub_list = []
            for item in d['children'][category_list.index(category)]['children']:
                sub_list.append(item['name'])

            if not sub_category in sub_list:
                d['children'][category_list.index(category)]['children'].append({"name":sub_category, "children":[{"name": sub_category_type, "size" : count}]})
            else:
                d['children'][category_list.index(category)]['children'][sub_list.index(sub_category)]['children'].append({"name": sub_category_type, "size" : count})

    # Create Directory and Save Files
    directory = 'visualisation/{}/'.format(domain.replace('.', ''))
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Save domain and number of URLs
    with open('{}metadata.json'.format(directory), 'w') as outfile:
        json.dump({'domain': domain, 'no_of_urls': len(page_urls)}, outfile)

    # Save flare file
    with open('{}flare.json'.format(directory), 'w') as outfile:
        json.dump(d, outfile)

    # Load and create index.html file
    with open("visualisation/main/index.html") as inf:
        txt = inf.read()
        soup = bs4.BeautifulSoup(txt,"html.parser")

    with open("{}index.html".format(directory), "w") as outf:
        outf.write(str(soup))

    print('Visualisation hosted at {}'.format(directory))

def VisualiseSitemap(page_urls):
    page_urls, domain = structure_url(page_urls)
    df = parent_to_child_url(page_urls)
    dataframe_to_flare(df,page_urls,domain)
