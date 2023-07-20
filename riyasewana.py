import re
import requests
import csv
import time

def scrape_riyasewana():
    csv_content = "Title,SubTitle,Location,PostedDate,Url,Price,Contact,YOM,Make,Model,Mileage,Gear,Fuel Type,Engine\n"

    session = requests.Session()
    session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"

    for page in range(2, 3):  # Only scrape the first page (you can modify the range as needed)
        base_url = f"https://riyasewana.com/search/cars?page={page}"
        print("Base URL:", base_url)

        # Add delay between requests
        time.sleep(2)

        response = session.get(base_url)
        # print("Response:", response)
        content = response.text
        # print("Content:", content)

        car_ads = extract_car_links_from_response(content)
        print(f"Car Ads: {car_ads}")

        for i, car_ad in enumerate(car_ads):
            print(f"Processing Car Ad {i + 1}: {car_ad}")

            # Add delay between requests
            time.sleep(2)

            response = session.get(car_ad)
            # print("Ad Details Response:", response)
            content = response.text

            # # Specify the file path
            # file_path = "output.txt"

            # # Write the content to a file
            # with open(file_path, "w") as file:
            #     file.write(content)

            # Print a confirmation message
            # print("Content has been written to the file:", file_path)

            price_pattern = r"Price:\sRs.\s([\d,.]+)"
            contact_pattern = r"Contact<\/p><\/td><td class=\"aleft tfiv\"><span class=\"moreph\">([\d\s]+)"
            yom_pattern = r"YOM<\/p><\/td><td class=\"aleft\">(\d{4})"
            make_pattern = r"Make<\/p><\/td><td class=\"aleft tfiv\">(.*?)<\/td>"
            model_pattern = r"Model<\/p><\/td><td class=\"aleft\">(.*?)<\/td>"
            mileage_pattern = r"Mileage \(km\)<\/p><\/td><td class=\"aleft\">(.*?)<\/td>"
            gear_pattern = r"Gear<\/p><\/td><td class=\"aleft\">(.*?)<\/td>"
            fuel_type_pattern = r"Fuel Type<\/p><\/td><td class=\"aleft\">(.*?)<\/td>"
            engine_pattern = r"Engine \(cc\)<\/p><\/td><td class=\"aleft\">(.*?)<\/td>"
            title_pattern= r"<title>(.*?)<\/title>"
            sub_pattern = r'<div id="mbody".*?>\s*<div id="content".*?>\s*<h1.*?>(.*?)</h1>\s*<h2.*?>(.*?)</h2>'
            # Define the pattern to match the date and time
            postedDate_pattern = r"\d{4}-\d{2}-\d{2} \d{1,2}:\d{2} [ap]m"


            price_match = re.search(price_pattern, content)
            contact_match = re.search(contact_pattern, content)
            yom_match = re.search(yom_pattern, content)
            make_match = re.search(make_pattern, content)
            model_match = re.search(model_pattern, content)
            mileage_match = re.search(mileage_pattern, content)
            gear_match = re.search(gear_pattern, content)
            fuel_type_match = re.search(fuel_type_pattern, content)
            engine_match = re.search(engine_pattern, content)
            title_match= re.search(title_pattern, content)
            sub_match = re.search(sub_pattern, content, re.DOTALL)
            


            

            price = price_match.group(1) if price_match else "NA"
            contact = contact_match.group(1) if contact_match else "NA"
            yom = yom_match.group(1) if yom_match else "NA"
            make = make_match.group(1) if make_match else "NA"
            model = model_match.group(1) if model_match else "NA"
            mileage = mileage_match.group(1) if mileage_match else "NA"
            gear = gear_match.group(1) if gear_match else "NA"
            fuel_type = fuel_type_match.group(1) if fuel_type_match else "NA"
            engine = engine_match.group(1) if engine_match else "NA"
            title=title_match.group(1) if title_match else "NA"
            subTitle=sub_match.group(2) if sub_match else "NA"
            # Extract the location after the comma
            location = subTitle.split(",")[-1].strip() if subTitle != "NA" else "NA"
            subTitle=sub_match.group(2).replace(",", "") if sub_match else "NA"

            postedMatch=re.search(postedDate_pattern, subTitle)
            postedDate= postedMatch.group(0) if postedMatch else "NA"

            print("Price:", price)
            print("Contact:", contact)
            print("YOM:", yom)
            print("Make:", make)
            print("Model:", model)
            print("Mileage:", mileage)
            print("Gear:", gear)
            print("Fuel Type:", fuel_type)
            print("Engine:", engine)
            print("Title:", title)
            print("Sub Title:" ,subTitle)
            print("Location:", location)
            print("Posted Date:", postedDate)
            print("url:",car_ad)
            
            csv_content += f"{title},{subTitle},{location},{postedDate},{car_ad},{price},{contact},{yom},{make},{model},{mileage},{gear},{fuel_type},{engine}\n"

    print("CSV content:")
    print(csv_content)

    # Save the CSV file
    with open("Riyasewana-test.csv", "w") as csv_file:
        csv_file.write(csv_content)

def extract_car_links_from_response(content):
    regex = r"<li[^>]*>\s*<[^>]*>\s*<a[^>]*href=\"(.*?)\""
    matches = re.findall(regex, content)
    return matches

scrape_riyasewana()
