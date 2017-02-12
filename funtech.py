import tweepy
import time
import sqlite3
from datetime import date
from textblob import TextBlob
from creds import TWITTER_API_KEY, TWITTER_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

companies = ['RBC','3M Company', 'AbbVie', 'Accenture plc', 'Activision Blizzard', 'Adobe Systems ', 'AES ', 'Aetna ', 'AFLAC ', 'Agilent Technologies ', 'Albemarle ', 'Alcoa ', 'Alexion Pharmaceuticals', 'Allegion', 'Allergan plc', 'Alliant Energy ', 'Allstate ', 'Alphabet Inc Class A', 'Altria Group ', 'Amazon ', 'Ameren ', 'Ameriprise Financial', 'AmerisourceBergen ', 'Ametek', 'Amgen ', 'Amphenol Corp A', 'Anadarko Petroleum ', 'Aon plc', 'Apache Corporation', 'Apple ', 'Applied Materials ', 'Archer-Daniels-Midland ', 'Arthur J. Gallagher & ', 'Assurant ', 'AT&T ', 'Autodesk ', 'AutoNation ', 'AutoZone ', 'Avago Technologies', '"AvalonBay Communities', 'Avery Dennison ', 'Baker Hughes ', 'Ball ', 'Bank of America ', 'BB&T Corporation', 'Becton Dickinson', 'Bed Bath & Beyond', 'Berkshire Hathaway', 'Best Buy Co. ', 'BIOGEN IDEC ', 'BlackRock', 'Block H&R', 'Boeing Company', 'BorgWarner', 'Boston Properties', 'C. H. Robinson Worldwide', '"CA', 'Cabot Oil & Gas', 'Campbell Soup', 'Capital One Financial', 'Cardinal Health ', 'Carmax ', 'Carnival ', 'Caterpillar ', 'CBRE ', 'CBS ', 'Celgene ', 'Centene Corporation', 'CenterPoint Energy', 'CenturyLink ', 'Cerner', 'CF Industries Holdings ', 'Charles Schwab Corporation', 'Chesapeake Energy', 'Chevron ', 'Chipotle Mexican Grill', 'Chubb Limited', 'Church & Dwight', 'CIGNA ', 'Cimarex Energy', 'Cincinnati Financial', 'Cintas Corporation', 'Cisco Systems', 'Citigroup ', 'Citizens Financial ', 'Citrix Systems', 'CME Group ', 'CMS Energy', 'Coach ', 'Cognizant Technology Solutions', 'Colgate-Palmolive', 'Comcast A ', 'Comerica ', 'ConAgra Foods ', 'Concho Resources', 'ConocoPhillips', 'Consolidated Edison', 'Constellation Brands', 'Corning ', 'Costco ', 'CSRA ', 'CSX ', 'Cummins ', 'CVS Health', 'D. R. Horton', 'Danaher ', 'Darden Restaurants', 'DaVita ', 'Deere & ', 'Delphi Automotive', 'Delta Air Lines', 'Dentsply Sirona', 'Devon Energy ', 'Diamond Offshore Drilling', 'Digital Realty Trust', 'Discover Financial ', 'Dollar General', 'Dollar Tree', 'Dominion Resources', 'Dover ', 'Dow Chemical', 'Dr Pepper Snapple ', 'DTE Energy ', 'E*Trade', 'Eastman Chemical', 'Eaton Corporation', 'eBay ', 'Ecolab ', "Edison Int'l", 'Edwards Lifesciences', 'Electronic Arts', 'EMC ', 'Emerson Electric Company', 'Endo International', 'Entergy ', 'EOG Resources', 'EQT Corporation', 'Equifax ', 'Equinix', 'Equity Residential', 'Essex Property Trust ', 'Estee Lauder Cos.', 'Eversource Energy', 'Exelon ', 'Expedia ', "Expeditors Int'l", 'Express Scripts', 'Extra Space Storage', 'Exxon Mobil ', 'F5 Networks', 'Facebook', 'Fastenal ', 'Federal Realty Investment Trust', 'FedEx Corporation', 'Fifth Third Bancorp', 'First Solar ', 'FirstEnergy ', 'Fiserv ', 'FLIR Systems', 'Flowserve Corporation', 'FMC Technologies ', 'Foot Locker ', 'Ford Motor', 'Fortive ', 'Fortune Brands Home & Security', 'Franklin Resources', 'Freeport-McMoran Cp & Gld', 'Frontier Communications', 'Gap (The)', 'Garmin Ltd.', 'Gilead Sciences', 'Global Payments ', 'Goldman Sachs ', 'Goodyear Tire & Rubber', 'Harley-Davidson', 'Hartford Financial Svc.Gp.', 'Hasbro ', 'HCA Holdings', 'HCP ', 'Helmerich & Payne', 'Henry Schein', 'Hess Corporation', 'Hewlett Packard Enterprise', 'Hologic', 'Home Depot', "Honeywell Int'l ", 'Hormel Foods ', 'Host Hotels & Resorts', 'HP ', 'Humana ', 'Huntington Bancshares', 'Illinois Tool Works', 'Illumina ', 'Ingersoll-Rand PLC', 'Intel ', 'Intercontinental Exchange', 'International Bus. Machines', 'International Paper', 'Interpublic ', 'Intl Flavors & Fragrances', 'Intuit ', 'Intuitive Surgical ', 'Invesco Ltd.', 'Iron Mountain Incorporated', 'J. B. Hunt Transport ', 'Johnson & Johnson', 'Johnson Controls', 'JPMorgan Chase & ', 'Juniper Networks', 'Kansas City Southern', 'Kimberly-Clark', 'Kimco ', 'Kinder Morgan', 'KLA-Tencor ', "Kohl's ", 'Kraft Heinz ', 'Kroger ', 'L Brands ', 'L-3 Communications Holdings', 'Laboratory Corp. of America Holding', 'Lam Research', 'Legg Mason', 'Linear Technology ', 'LKQ Corporation', 'Lockheed Martin ', 'Loews ', 'LyondellBasell', 'M&T Bank ', 'Macerich', "Macy's ", 'Mallinckrodt Plc', 'Marathon Oil ', 'Marathon Petroleum', "Marriott Int'l.", 'Martin Marietta Materials', 'Masco ', 'Mastercard ', 'McCormick & ', "McDonald's ", 'McKesson ', 'Mead Johnson', 'Medtronic plc', 'Merck & ', 'MetLife ', 'Michael Kors Holdings', 'Microchip Technology', 'Micron Technology', 'Microsoft ', 'Molson Coors Brewing Company', 'Mondelez International', 'Monsanto ', 'Monster Beverage', "Moody's ", 'Morgan Stanley', 'Motorola Solutions ', 'Murphy Oil', 'Mylan N.V.', 'NASDAQ OMX ', 'National Oilwell Varco ', 'Navient', 'NetApp', 'Netflix ', 'Newell Rubbermaid ', 'Newfield Exploration ', 'Newmont Mining Corp. (Hldg. Co.)', 'NextEra Energy', 'Nielsen Holdings', 'Nike', 'NiSource ', 'Noble Energy ', 'Nordstrom', 'Norfolk Southern ', 'Northern Trust ', 'Northrop Grumman ', 'NRG Energy', 'Nucor ', 'Nvidia Corporation', 'ONEOK', 'Oracle ', 'PACCAR ', 'Patterson Companies', 'Paychex ', 'PayPal', 'Pentair Ltd.', 'PepsiCo ', 'Perrigo', 'Pfizer ', 'PG&E ', 'Philip Morris International', 'Phillips 66', 'Pinnacle West Capital', 'PPG Industries', 'PPL ', 'Praxair ', 'Priceline.com ', 'Principal Financial ', 'Procter & Gamble', 'Progressive ', 'Prologis', 'Prudential Financial', 'Public Serv. Enterprise ', 'Public Storage', 'Pulte Homes ', 'PVH ', 'Qorvo', 'QUALCOMM ', 'Quanta Services ', 'Quest Diagnostics', 'Range Resources ', 'Raytheon ', 'Realty Income Corporation', 'Red Hat ', 'Ross Stores', 'Royal Caribbean Cruises Ltd', 'Ryder System', '"S&P Global', 'Salesforce.com', 'Sempra Energy', 'Sherwin-Williams', 'Signet Jewelers', 'Simon Property Group ', 'Skyworks Solutions', 'SL Green ', 'Smucker (J.M.)', 'Snap-On ', 'Southern ', 'Southwest Airlines', 'Southwestern Energy', 'Spectra Energy ', 'St Jude Medical', 'Stanley Black & Decker', 'Staples ', 'Starbucks ', 'State Street ', 'Stericycle ', 'Stryker ', 'SunTrust Banks', 'Symantec ', 'Synchrony Financial', 'Sysco ', 'T. Rowe Price ', 'Target ', 'Tesoro Petroleum ', 'Texas Instruments', 'Textron ', 'The Coca Cola Company', 'The Hershey Company', 'The Mosaic Company', 'The Travelers Companies ', 'The Walt Disney Company', 'Tiffany & ', 'Time Warner ', 'TJX Companies ', 'Torchmark ', 'Total System ', 'Tractor Supply Company', 'TransDigm ', 'Transocean', 'TripAdvisor', 'Tyco International', 'Tyson Foods', 'U.S. Bancorp', 'UDR ', 'Ulta Salon Cosmetics & Fragrance ', 'Under Armour', 'Union Pacific', 'United Technologies', '"Universal Health ', 'Unum ', 'Urban Outfitters', 'V.F. ', 'Valero Energy', 'Varian Medical Systems', 'Ventas ', 'Verisign ', 'Viacom ', 'Visa ', 'Vornado Realty Trust', 'Wal-Mart Stores', 'Walgreens Boots Alliance', 'Waste Management ', 'Waters Corporation', 'Wells Fargo', 'Welltower ', 'Western Digital', 'Western Union ', 'Westrock ', 'Williams Cos.', 'Willis Towers Watson', 'Wisconsin Energy Corporation', 'Xcel Energy ', 'Xerox ', 'Xilinx ', 'XL Capital', 'Xylem ', 'Yahoo ', 'Zimmer Biomet Holdings', 'Zions Bancorp', 'Zoetis']

conn = sqlite3.connect('funtech.db')

conn.execute("CREATE TABLE IF NOT EXISTS sentiments (date TEXT, company TEXT, sentiment FLOAT)")

auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

current = time.time()
buffer = {}

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        global current
        global buffer
        for company in companies:
            if company in status.text:
                stmt = TextBlob(status.text)
                sent = stmt.sentiment.polarity
                if(company in buffer):
                    count, average_sent = buffer[company]
                    count += 1
                    average_sent = (count*average_sent + sent)/(count+1)
                    buffer[company] = (count, average_sent)
                else:
                    buffer[company] = (1, sent)
                break
        else:
            return
        print(status.text)
        if(abs(current - time.time()) > 40):
            for company, (count, average_sent) in buffer.items():
                conn.execute("insert into sentiments values (?, ?, ?)", (str(date.today()), company, average_sent))
            conn.commit()
            buffer = {}
            current = time.time()
        
    def on_error(self, status_code):
        if status_code == 420:
            return False

myStream = tweepy.Stream(auth = api.auth, listener=MyStreamListener())

myStream.filter(track=companies)