import json
import requests


# curl -X POST https://api.notion.com/v1/databases/notion_database_id/query

# -H 'Authorization: Bearer '"secret_api_key"''

# -o database.json 

DATABASE_ID = "database_id"
# NOTION_URL = 'https://api.notion.com/v1/databases/'

# NOTION_URL = 'https://api.notion.com/v1/databases/'
token = 'secret_4ZXOngRoHVm1gNdKLvUZXgIeJw8OGfDqGBzvIy7Zxy0'
databaseId = '78f68cce00614a07bd8428ebd451ca1f'
pageID = '6f9dd769-d042-433d-b9b2-29172edbb43c'
headers = {
    "Authorization": "Bearer " +token,
    "Notion-Version": "2021-08-16"
}

class NotionSync:
    def __init__(self):
        pass    

    # Function will query a database and return all elements in one list
    def query_databases(self,integration_token="secret_4ZXOngRoHVm1gNdKLvUZXgIeJw8OGfDqGBzvIy7Zxy0"):
        database_url = f"https://api.notion.com/v1/databases/{databaseId}/query"
        header = {
            "Authorization": "Bearer " + integration_token,
            "Notion-Version": "2021-08-16"
        }
        # Queries the database to get first block of data
        # notion will send up to 100 elements meaning that 
        # one will need to query the database several times
        # moving the start cursor in order to attain all data
        # from the database
        response = requests.post(database_url, headers=header)
        if response.status_code != 200:
            print(response.status_code)
        else:
            # conversion will hold the database response data
            conversion = response.json()
            # data_dump will be a buffer holding all of the rows from the database
            data_dump = conversion["results"]
            # print(len(conversion["results"]))
            # while there is still more rows in the database keep quering
            # and concatinate the data to the buffer
            while conversion["has_more"]:
                response = requests.post(database_url, headers=header, json={
                    "start_cursor": conversion["next_cursor"]
                }
                )
                if response.status_code != 200:
                    print(response.status_code)
                else:
                    # set conversion to new response from database
                    conversion = response.json()
                    data_dump = data_dump + conversion["results"]
            return data_dump
    # Function iterates through the values in the database in order to attain wanted plottable information
    def get_important_information(self, data_json):
        bank = {
        "Resource": [],
        "Status": [],
        "Completed Date": [],
        "Actual Start Date": [],
        "Projected Due Date": [],
        "Last Updated": [],
        "Projected Start Date": [],
        "Priority": [],
        "Name": [],
        "Epic": []
        }
        data_json.reverse()
        # ask about epic
        for i in data_json:
            # Filling up the Status:
            if i["properties"]["Status"]["select"]:
                bank["Status"].append(i["properties"]["Status"]["select"]["name"])
            else:
                bank["Status"].append(None)
            # Filling up the Completed Date:
            if (i["properties"]["Status"]
            ["select"] and i["properties"]
            ["Status"]["select"]["name"] ==
            "Completed" and i["properties"]["Completed Date"]["date"]
            and i["properties"]["Completed Date"]["date"]["start"]):
                bank["Completed Date"].append(i["properties"]["Completed Date"]["date"]["start"])
            else:
                bank["Completed Date"].append(None)
            # Filling up the Actual Start Dates:
            if i["properties"]["Actual Start Date"]["date"]:
                bank["Actual Start Date"].append(i["properties"]["Actual Start Date"]["date"]["start"])
            else:
                bank["Actual Start Date"].append(None)
            # Filling up Projected Due Dates:
            if i["properties"]["Projected Due Date"]["date"]:
                bank["Projected Due Date"].append(i["properties"]["Projected Due Date"]["date"]["start"])
            else:
                bank["Projected Due Date"].append(None)
            # Filling up Last Updated dates:
            if i["properties"]["Last Updated"]["last_edited_time"]:
                bank["Last Updated"].append(i["properties"]["Last Updated"]["last_edited_time"])
            else:
                bank["Last Updated"].append(None)
            # Filling up Projected Start Dates:
            if (i["properties"]["Projected Start Date"]["date"]
            and i["properties"]["Projected Start Date"]["date"]["start"]):
                bank["Projected Start Date"].append(i["properties"]["Projected Start Date"]["date"]["start"])
            else:
                bank["Projected Start Date"].append(None)
            # Filling up resources:
            if i["properties"]["Resource"]["people"]:
                bank["Resource"].append(i["properties"]["Resource"]["people"][0]["name"])
            else:
                bank["Resource"].append(None)
            # Filling up Priorities:
            if i["properties"]["Priority"]["select"]:
                bank["Priority"].append(i["properties"]["Priority"]["select"]["name"]) 
            else:
                bank["Priority"].append(None)
            # Filling up Name:
            if i["properties"]["Name"]["title"]:
                bank["Name"].append(i["properties"]["Name"]["title"][0]["plain_text"]) 
            else:
                bank["Name"].append(None)
            # Filling up Epic:
            if i["properties"]["Epic"]["relation"]:
                bank["Epic"].append(i["properties"]["Epic"]["relation"][0]["id"])
            else:
                bank["Epic"].append(None)

        # print(bank.keys())
        return bank

if __name__=='__main__':
    nsync = NotionSync()
    data = nsync.query_databases()
    info = nsync.get_important_information(data)

