import requests
import pandas as pd
import urllib
import os
from time import sleep
from selenium import webdriver
import argparse
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
print "Starting program..."
argparser = argparse.ArgumentParser()
argparser.add_argument("--password", help="Enter your Facebook password")
argparser.add_argument("--email", help="Enter your Facebook email")
argparser.add_argument("--profiles", help="Add already build profile CSV file.", default="None")
argparser.add_argument("--member_ids", help="List of group members.", default="None")
argparser.add_argument("--speed", help="Set a number between 2 and 10 for how SLOW you want the program to run", default=2)
argparser.add_argument("--token", help="Enter your API token")
args = argparser.parse_args()

token = args.token
log_name = args.email
log_pass = args.password
sleep_time = args.speed
profile_df = args.profiles
group_df = args.member_ids


def get_members(group_id):
    member_dict = {"group_id": [], "member_name": [], "member_id": [], "admin": []}
    url = "https://graph.facebook.com/v2.9/%s/members?access_token=%s" % (group_id, token)
    r = requests.get(url)
    r = r.json()
    print r
    try:
        next_token = r['paging']['next']
    except Exception as e:
        print e
        next_token = "last_page"
    try:

        for member in r['data']:
            member_dict['group_id'].append(group_id)
            member_dict['admin'].append(member['administrator'])
            member_dict['member_name'].append(member['name'])
            member_dict['member_id'].append(member['id'])
    except Exception as e:
        print e
        pass

    return(next_token, member_dict)


def paginate(next_token, group_id):
    member_dict = {"group_id": [], "member_name": [], "member_id": [], "admin": []}
    r = requests.get(next_token)
    r = r.json()
    print r
    try:
        next_token = r['paging']['next']
    except:
        next_token = "last_page"
    try:

        for member in r['data']:
            member_dict['group_id'].append(group_id)
            member_dict['admin'].append(member['administrator'])
            member_dict['member_name'].append(member['name'])
            member_dict['member_id'].append(member['id'])
    except:
        pass

    return (next_token, member_dict)



def get_profile_groups():
    driver.find_element_by_xpath('//a[@title="Profile"]').click()
    sleep(2)
    driver.find_element_by_xpath("//a[contains(.,'About')]").click()

    try:
        current_url = str(driver.current_url)
        current_url = current_url.replace("about", "groups").strip()
        print "getting " + current_url
        driver.get(current_url)
        sleep(1)
    except:
        print "error finding profile groups"

    all_groups = []
    groups = driver.find_element_by_id("pagelet_timeline_medley_groups")
    group_links = groups.find_elements_by_tag_name("a")
    for link in group_links:
        try:
            link_id = link.get_attribute("data-hovercard")
            link_id = link_id.split("=")
            link_id = link_id[1]
            all_groups.append(link_id)
        except:
            pass
    print "Found " + str(len(all_groups)) + " groups."
    return all_groups



def login(mylog, mypass):
    print "Logging into Facebook."
    driver.get(url)
    login = driver.find_element_by_id("email")
    passwd = driver.find_element_by_id("pass")
    logbutton = driver.find_element_by_id("loginbutton")
    mylog = "spn259@nyu.edu"
    mypass = "Lamerced0257!"

    login.send_keys(mylog)
    passwd.send_keys(mypass)
    logbutton.click()


def get_profile_info(member_id, name):

    prof_dict = {"member_id":[], "name":[], "work_1":[], "link_work_1":[], "position_work_1":[], "work_2":[], "link_work_2":[], "position_work_2":[],  "work_3":[], "link_work_3":[], "position_work_3":[], "current_city":[], "address":[], "website":[], "phone":[], "email":[], "birthday":[], "about":[], "quotes":[]}
    driver.find_element_by_xpath("//a[contains(.,'About')]").click()
    sleep(sleep_time)
    try:
        driver.find_element_by_xpath("//a[contains(.,'Work and Education')]").click()
    except Exception as e:
        sleep(sleep_time)
        try:
            driver.find_element_by_xpath("//a[contains(.,'Work and Education')]").click()
        except Exception as e:
            pass

    prof_dict['member_id'].append(member_id)
    prof_dict['name'].append(name)
    sleep(sleep_time)
    try:
        work = driver.find_element_by_id("pagelet_eduwork")
        work_list = work.find_element_by_tag_name("ul")
        work_list = work_list.find_elements_by_tag_name("li")
        print str(len(work_list)) + " jobs"
    except Exception as e:
        pass

    try:
        first_work = work_list[0]
        work_1 = first_work.text
        prof_dict['work_1'].append(work_1.split()[0])
        prof_dict['link_work_1'].append(first_work.find_element_by_tag_name("a").get_attribute("href"))
        prof_dict['position_work_1'].append(first_work.find_element_by_class_name("_173e").text)

        try:
            second_work = work_list[1]
            work_2 = second_work.text
            prof_dict['work_2'].append(work_2.split()[0])

            prof_dict['work_2'].append(second_work.find_element_by_tag_name("a").text)
            prof_dict['link_work_2'].append(second_work.find_element_by_tag_name("a").get_attribute("href"))
            prof_dict['position_work_2'].append(second_work.find_element_by_class_name("_173e").text)


            try:
                third_work = work_list[2]
                work_3 = first_work.text
                prof_dict['work_3'].append(work_3.split()[0])
                prof_dict['work_3'].append(third_work.find_element_by_tag_name("a").text)
                prof_dict['link_work_3'].append(third_work.find_element_by_tag_name("a").get_attribute("href"))
                prof_dict['position_work_3'].append(third_work.find_element_by_class_name("_173e").text)


            except Exception as e:
                pass

        except Exception as e:
            pass

    except Exception as e:
        pass



    try:
        driver.find_element_by_xpath("//span[contains(.,'Lived')]").click()
        sleep(sleep_time)
        current_city = driver.find_element_by_id("current_city").text
        current_city = current_city.replace("Current city", "").strip()
        prof_dict['current_city'].append(current_city)
    except Exception as e:
        print e
        pass


    sleep(sleep_time)
    try:

        basic_section = driver.find_element_by_id("u_jsonp_2_0")
        basic_list = basic_section.find_elements_by_tag_name("span")
        basic_list = [x.text for x in basic_list]
        for i, item in enumerate(basic_list):
            print item
            if "Address" in item:
                prof_dict['address'].append(basic_list[i+1])
            elif "Website" in item:
                website = basic_list[i+1]
                prof_dict['website'].append(basic_list[i+1])
            elif "Phone" in item:
                prof_dict['phone'].append(basic_list[i+1])
            elif "mail" in item:
                prof_dict['email'].append(basic_list[i+1])
            elif "Birthday" in item:
                prof_dict['birthday'].append(basic_list[i+1])
            else:
                pass
    except Exception as e:
        print e
        pass

        # driver.find_element_by_xpath("//a[contains(.,'Details About')]").click()
    try:
        current_url = str(driver.current_url)
        current_url = current_url.split("&section=")
        current_url = current_url[0] + "&section=bio&pnref=about"
        driver.get(current_url)
        sleep(sleep_time)
    except Exception as e:
        print e
        pass

    try:
        about_section = driver.find_element_by_id("pagelet_bio")
        about_list = about_section.find_elements_by_tag_name("span")
        try:
            about_list = [x.text for x in about_list]
            for i, item in enumerate(about_list):
                print item
                if "No additional" in item or "ABOUT" in item:
                    print "No About Section"
                    continue
                elif item != "" and item not in prof_dict['about']:
                    prof_dict['about'].append(about_list[i])
                else:
                    pass
        except Exception as e:
            print e
            pass
    except Exception as e:
        print e
        pass



    try:
        quotes_section = driver.find_element_by_id("pagelet_quotes")
        quotes_list = quotes_section.find_elements_by_tag_name("span")
        try:
            quotes_list = [x.text for x in quotes_list]
            for i, item in enumerate(quotes_list):
                print item
                if "No additional" in item or "QUOTES" in item:
                    print "No Quotes Section"
                    continue
                elif item != "" and item not in prof_dict['quotes']:
                    prof_dict['quotes'].append(item)
                else:
                    pass
        except Exception as e:
            print e
            pass
    except Exception as e:
        print e
        pass


    temp_df = pd.DataFrame.from_dict(prof_dict, orient='index')
    temp_df = temp_df.transpose()
    correct_cols = ['member_id', 'name', 'work_1', 'link_work_1', 'position_work_1', 'work_2', 'link_work_2', 'position_work_2', 'work_3', 'link_work_3', 'position_work_3', 'current_city', 'address', 'website', 'phone', 'email', 'birthday', 'about', 'quotes']
    temp_df = temp_df[correct_cols]
    print temp_df
    return temp_df


def grab_all_profiles():
    profile_df = pd.DataFrame()
    for index, row in group_df.iterrows():
        current_pass = 0
        if row['member_id'] not in current:
            print "currently scraping profile number "+ str(index)
            try:
                fburl = "https://www.facebook.com/"+str(row['member_id'])
                print fburl
                driver.get(fburl)

                temp_df = get_profile_info(row['member_id'], row['member_name'])
                profile_df = profile_df.append(temp_df)
                current_pass += 1
            except Exception as e:
                print "error"
                print e
                pass
            while current_pass >= 100:
                login(mylog,mypass)
                current_pass = 0


        else:
            print "Already scraped this person."
            pass

    return profile_df








url = "http://www.facebook.com/"
# driver = webdriver.PhantomJS() # or a

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option('prefs', {
    'credentials_enable_service': False,
    'profile': {
        'password_manager_enabled': False
    }
})
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)

login(log_name, log_pass)
if group_df == "None":
    all_groups = get_profile_groups()
    group_df = pd.DataFrame()
    for group in all_groups[0:3]:
        print "Using Facebook API to retrieve members of groups. This may take a second."
        res = get_members(group)
        temp_group_df = pd.DataFrame.from_dict(res[1], orient='index')
        temp_group_df = temp_group_df.transpose()
        print temp_group_df

        while res[0] != "last_page":
            res = paginate(res[0], group)
            temp_df = pd.DataFrame.from_dict(res[1], orient='index')
            temp_df = temp_df.transpose()
            print "adding " + str(len(temp_df)) + " to " + str(len(temp_group_df))
            temp_group_df = temp_group_df.append(temp_df, ignore_index=False)

    group_df = group_df.append(temp_group_df)

else:
    print "Reading groups from file."
    group_df = pd.read_csv(group_df)


print "There are a total of "+str(len(group_df))+ " profiles to scrape."
print "Saving group information to CSV file."
group_df.to_csv("group_members.csv", sep=",", encoding='utf-8', index=False)

if profile_df != "None":
    print "Reading profiles from file."
    profile_df = pd.read_csv(profile_df)
    current = list(profile_df.member_id)
    temp_df = grab_all_profiles()
    profile_df = profile_df.append(temp_df)
else:
    current = []
    profile_df = grab_all_profiles()

print "Saving output to a CSV file."
profile_df.to_csv("profiles.csv", sep=",", encoding='utf-8', index=False)

