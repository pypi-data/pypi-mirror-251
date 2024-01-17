# Examples of Using ZAT

This documents shows a wide variety of ways to use the ZAT toolkit to process Zeek output.

-   Any Zeek Log into Python (dynamic tailing and log rotations are handled)
-   Zeek Logs to Pandas Dataframes and Scikit-Learn
-   Dynamically monitor files.log and make VirusTotal Queries
-   Dynamically monitor http.log and show 'uncommon' User Agents
-   Running Yara Signatures on Extracted Files
-   Checking x509 Certificates
-   Anomaly Detection

### Pull in Zeek Logs as Python Dictionaries (examples/zeek\_pprint.py)

```python
from zat import zeek_log_reader
...
    # Run the zeek reader on a given log file
    reader = zeek_log_reader.ZeekLogReader('dhcp.log')
    for row in reader.readrows():
        pprint(row)
```

**Output:** Each row is a nice Python Dictionary with timestamps and
types properly converted.

    {'assigned_ip': '192.168.84.10',
    'id.orig_h': '192.168.84.10',
    'id.orig_p': 68,
    'id.resp_h': '192.168.84.1',
    'id.resp_p': 67,
    'lease_time': datetime.timedelta(49710, 23000),
    'mac': '00:20:18:eb:ca:54',
    'trans_id': 495764278,
    'ts': datetime.datetime(2012, 7, 20, 3, 14, 12, 219654),
    'uid': 'CJsdG95nCNF1RXuN5'}
    ...

### Zeek log to Pandas DataFrame (examples/zeek\_to\_pandas.py)

```python
from zat.log_to_dataframe import LogToDataFrame
...
    # Create a Pandas dataframe from a Zeek log
    log_to_df = LogToDataFrame()
    zeek_df = log_to_df.create_dataframe('/path/to/dns.log')

    # Print out the head of the dataframe
    print(zeek_df.head())
```

**Output:** All the Zeek log data is in a Pandas DataFrame with proper
types and timestamp as the index

```
                                                    query      id.orig_h  id.orig_p id.resp_h
ts
2013-09-15 17:44:27.631940                     guyspy.com  192.168.33.10       1030   4.2.2.3
2013-09-15 17:44:27.696869                 www.guyspy.com  192.168.33.10       1030   4.2.2.3
2013-09-15 17:44:28.060639   devrubn8mli40.cloudfront.net  192.168.33.10       1030   4.2.2.3
2013-09-15 17:44:28.141795  d31qbv1cthcecs.cloudfront.net  192.168.33.10       1030   4.2.2.3
2013-09-15 17:44:28.422704                crl.entrust.net  192.168.33.10       1030   4.2.2.3
```
### Filter out DNS Whitelists (examples/pandas\_whitelist.py)

```python
from zat.log_to_dataframe import LogToDataFrame
...
   # Create a Pandas dataframe from a Zeek log
   log_to_df = LogToDataFrame()
   zeek_df = log_to_df.create_dataframe(args.dns_log)

   # Grab the whitelist
   white_df = pd.read_csv(args.whitelist, names=['rank', 'domain'])
   whitelist = white_df['domain'].tolist()

   # Filter the dataframe with the whitelist
   zeek_df = zeek_df[~zeek_df['query'].isin(whitelist)]
```

**Example usage/output**

```
$ python pandas_whitelist.py ../data/dns.log ../data/top_domains_1k.csv
DF Size before whitelist: 54 rows
Filtering out ['stats.g.doubleclick.net', 'www.googletagservices.com', 
   'partner.googleadservices.com',  'www.google-analytics.com', 
   'pubads.g.doubleclick.net', 'pagead2.googlesyndication.com', 
   'ib.adnxs.com', 'googleads.g.doubleclick.net', 'www.facebook.com',
   'insight.adsrvr.org', 'ad.doubleclick.net', 'www.google.com', 
   'ajax.googleapis.com', 's0.2mdn.net', 'www.google.com']
DF Size after whitelist: 39 rows
```
### Zeek Log to Scikit-Learn (examples/zeek\_to\_scikit.py)
See **zat/examples/zeek\_to\_scikit.py** for full code listing, we've shortened the code listing here to demonstrate that it's literally just a few lines of code to get to Scikit-Learn.

```python
# Create a Pandas dataframe from a Zeek log
log_to_df = LogToDataFrame()
zeek_df = log_to_df.create_dataframe('/path/to/dns.log')

# Use the DataframeToMatrix class (handles categorical data!)
to_matrix = dataframe_to_matrix.DataFrameToMatrix()
zeek_matrix = to_matrix.fit_transform(zeek_df)

# Now we're ready for scikit-learn!
kmeans = KMeans(n_clusters=5).fit_predict(zeek_matrix)
pca = PCA(n_components=2).fit_transform(zeek_matrix)
```

**Example Output**

    Rows in Cluster: 42
                               query  Z proto qtype_name         x         y  cluster
    0                     guyspy.com  0   udp          A -0.356148 -0.111347        0
    1                 www.guyspy.com  0   udp          A -0.488648 -0.068594        0
    2   devrubn8mli40.cloudfront.net  0   udp          A -0.471554 -0.110367        0
    3  d31qbv1cthcecs.cloudfront.net  0   udp          A -0.454148 -0.165611        0
    4                crl.entrust.net  0   udp          A -0.414992 -0.103959        0

    ...

    Rows in Cluster: 4
                query  Z proto qtype_name         x         y  cluster
    57  j.maxmind.com  1   udp          A -0.488136 -0.230034        3
    58  j.maxmind.com  1   udp          A -0.461758 -0.235828        3
    59  j.maxmind.com  1   udp          A -0.408193 -0.179723        3
    60  j.maxmind.com  1   udp          A -0.460889 -0.217559        3

    Rows in Cluster: 4
                                                    query  Z proto qtype_name         x         y  cluster
    53  superlongcrazydnsqueryforanomalydetectionj.max...  0   udp          A -0.554213 -0.206536        4
    54  xyzsuperlongcrazydnsqueryforanomalydetectionj....  0   udp          A -0.559984 -0.260327        4
    55  abcsuperlongcrazydnsqueryforanomalydetectionj....  0   udp          A -0.622886 -0.222030        4
    56  qrssuperlongcrazydnsqueryforanomalydetectionj....  0   udp          A -0.571959 -0.236560        4

### Zeek Files Log to VirusTotal Query

See zat/examples/file\_log\_vtquery.py for full code listing (code
simplified below)

```python
from zat import zeek_log_reader
from zat.utils import vt_query
...
    # Run the zeek reader on on the files.log output
    reader = zeek_log_reader.ZeekLogReader('files.log', tail=True) # This will dynamically monitor this Zeek log
    for row in reader.readrows():

        # Make the query with the file sha
        pprint(vtq.query(row['sha256']))
```

**Example Output:** Each file sha256/sha1 is queried against the
VirusTotal Service.

```
    {'file_sha': 'bdf941b7be6ba2a7a58b0aef9471342f8677b31c', 'not_found': True}
    {'file_sha': '2283efe050a0a99e9a25ea9a12d6cf67d0efedfd', 'not_found': True}
    {'file_sha': 'c73d93459563c1ade1f1d39fde2efb003a82ca4b',
        u'positives': 42,
        u'scan_date': u'2015-09-17 04:38:23',
        'scan_results': [(u'Gen:Variant.Symmi.205', 6),
            (u'Trojan.Win32.Generic!BT', 2),
            (u'Riskware ( 0015e4f01 )', 2),
            (u'Trojan.Inject', 2),
            (u'PAK_Generic.005', 2)]}

    {'file_sha': '15728b433a058cce535557c9513de196d0cd7264',
        u'positives': 33,
        u'scan_date': u'2015-09-17 04:38:21',
        'scan_results': [(u'Java.Exploit.CVE-2012-1723.Gen.A', 6),
            (u'LooksLike.Java.CVE-2012-1723.a (v)', 2),
            (u'Trojan-Downloader ( 04c574821 )', 2),
            (u'Exploit:Java/CVE-2012-1723', 1),
            (u'UnclassifiedMalware', 1)]}
```

### Zeek HTTP Log User Agents

See zat/examples/http\_user\_agents.py for full code listing (code
simplified below)

```python
from collections import Counter
from zat import zeek_log_reader
...
    # Run the zeek reader on a given log file counting up user agents
    http_agents = Counter()
    reader = zeek_log_reader.ZeekLogReader(args.zeek_log, tail=True)
    for count, row in enumerate(reader.readrows()):
        # Track count
        http_agents[row['user_agent']] += 1

    print('\nLeast Common User Agents:')
    pprint(http_agents.most_common()[:-50:-1])
```

**Example Output:** Might be some interesting agents on this list\...

    Least Common User Agents:
    [
     ('NetSupport Manager/1.0', 1),
     ('Mozilla/4.0 (Windows XP 5.1) Java/1.6.0_23', 1),
     ('Mozilla/5.0 (X11; Linux i686 on x86_64; rv:10.0.2) Gecko/20100101 Firefox/10.0.2', 1),
     ('oh sure', 2),
     ('Fastream NETFile Server', 2),
     ('Mozilla/5.0 (X11; Linux i686; rv:2.0.1) Gecko/20100101 Firefox/4.0.1', 3),
     ('Mozilla/5.0 (Windows NT 6.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1', 4),
     ('NESSUS::SOAP', 5),
     ('webmin', 6),
     ('Nessus SOAP v0.0.1 (Nessus.org)', 10),
     ('Mozilla/4.0 (compatible; gallery_203.nasl; Googlebot)', 31),
     ("mercuryboard_user_agent_sql_injection.nasl'", 31),
     ('Mozilla/5.0 (X11; Linux i686; rv:10.0.2) Gecko/20100101 Firefox/10.0.2', 46),
     ('*/*', 49),
     ('Nessus', 52),
     ...
     ('Mozilla/5.0 (compatible; Nmap Scripting Engine; http://nmap.org/book/nse.html)', 6166),

### Yara rules on Zeek extracted files

The example will dymancially monitor the extract\_files directory and
when a file is dropped by Zeek the code will run a set of Yara rules against that file. See zat/examples/yara\_matches.py for full code
listing (code simplified below)

```python
import yara
from zat import dir_watcher
...

def yara_match(file_path, rules):
    """Callback for a newly extracted file"""
    print('New Extracted File: {:s}'.format(file_path))
    print('Mathes:')
    pprint(rules.match(file_path))

...
    # Load/compile the yara rules
    my_rules = yara.compile(args.rule_index)

    # Create DirWatcher and start watching the Zeek extract_files directory
    print('Watching Extract Files Directory: {:s}'.format(args.extract_dir))
    dir_watcher.DirWatcher(args.extract_dir, callback=yara_match, rules=my_rules)
```

**Example Output:**

    Loading Yara Rules from ../zat/utils/yara_test/index.yar
    Watching Extract Files Directory: /home/ubuntu/software/zeek/extract_files
    New Extracted File: /home/ubuntu/software/zeek/extract_files/test.tmp
    Mathes:
    [AURIGA_driver_APT1]

### Risky Domains

The example will use the analysis in our [Risky
Domains](https://github.com/SuperCowPowers/zat/blob/main/notebooks/Risky_Domains.ipynb) notebook to flag domains that are 'at risk' and conduct a Virus Total query on those domains. See zat/examples/risky\_dns.py for full code
listing (code simplified below)

```python
from zat import zeek_log_reader
from zat.utils import vt_query
...

    # Create a VirusTotal Query Class
    vtq = vt_query.VTQuery()

    # See our 'Risky Domains' Notebook for the analysis and
    # statistical methods used to compute this risky set of TLDs
    risky_tlds = set(['info', 'tk', 'xyz', 'online', 'club', 'ru', 'website', 'in', 'ws', 'top', 'site', 'work', 'biz', 'name', 'tech'])

    # Run the zeek reader on the dns.log file looking for risky TLDs
    reader = zeek_log_reader.ZeekLogReader(args.zeek_log, tail=True)
    for row in reader.readrows():

        # Pull out the TLD
        query = row['query']
        tld = tldextract.extract(query).suffix

        # Check if the TLD is in the risky group
        if tld in risky_tlds:
            # Make the query with the full query
            results = vtq.query_url(query)
            if results.get('positives'):
                print('\nOMG the Network is on Fire!!!')
                pprint(results)
```

**Example Output:** To test this example simply do a \"\$ping uni10.tk\" on a machine being monitored by your Zeek.

Note: You can also ping something like 'isaftaho.tk' which is not on any of the blacklist but will still hit. The script will obviously cast a much wider net than just the blacklists.

```
$ python risky_dns.py -f /usr/local/var/spool/zeek/dns.log
Successfully monitoring /usr/local/var/spool/zeek/dns.log...

OMG the Network is on Fire!!!
{'filescan_id': None,
 'positives': 9,
 'query': 'uni10.tk',
 'scan_date': '2016-12-19 23:49:04',
 'scan_results': [('clean site', 55),
                  ('malicious site', 5),
                  ('unrated site', 4),
                  ('malware site', 4),
                  ('suspicious site', 1)],
 'total': 69,
 'url': 'http://uni10.tk/'}
```

### Cert Checker

There's been discussion about Let's Encrypt issuing certificates to possible phishing/malicious site owners. This example will quickly check
and dynamically monitor your Zeek x509 logs for certificates that may be from malicious sites.

See zat/examples/cert\_checker.py for full code listing (code simplified
below)

```python
from zat import zeek_log_reader
from zat.utils import vt_query
...

    # These domains may be spoofed with a certificate issued by 'Let's Encrypt'
    spoofed_domains = set(['paypal', 'gmail', 'google', 'apple','ebay', 'amazon'])

    # Run the zeek reader on the x509.log file looking for spoofed domains
    reader = zeek_log_reader.ZeekLogReader(args.zeek_log, tail=True)
    for row in reader.readrows():

        # Pull out the Certificate Issuer
        issuer = row['certificate.issuer']
        if "Let's Encrypt" in issuer:

            # Check if the certificate subject has any spoofed domains
            subject = row['certificate.subject']
            domain = subject[3:] # Just chopping off the 'CN=' part
            if any([domain in subject for domain in spoofed_domains]):
                print('\n<<< Suspicious Certificate Found >>>')
                pprint(row)

                # Make a Virus Total query with the spoofed domain (just for fun)
                results = vtq.query_url(domain)
                if results.get('positives', 0) >= 2: # At least two hits
                    print('\n<<< Virus Total Query >>>')
                    pprint(results)
```

**Example Output:** Simply run this example script on your Zeek x509.log.

    $ python cert_checker.py -f ../data/x509.log
      Successfully monitoring ../data/x509.log...

      <<< Suspicious Certificate Found >>>
      {'basic_constraints.ca': True,
       'certificate.issuer': "CN=Let's Encrypt Authority X3,O=Let's Encrypt,C=US",
       'certificate.key_alg': 'rsaEncryption',
       'certificate.key_length': 4096,
       'certificate.key_type': 'rsa',
       'certificate.sig_alg': 'sha256WithRSAEncryption',
       'certificate.subject': 'CN=paypal.migems.com',
       ...}

      <<< Virus Total Query >>>
      {'filescan_id': None,
       'positives': 8,
       'query': 'paypal.migems.com',
       'scan_date': '2017-04-16 09:39:52',
       'scan_results': [('clean site', 50),
                        ('phishing site', 6),
                        ('unrated site', 6),
                        ('malware site', 1),
                        ('malicious site', 1)],
       'total': 64,
       'url': 'http://paypal.migems.com/'}

### Anomaly Detection

Here we're demonstrating anomaly detection using the Isolated Forest
algorithm. Once anomalies are identified we then use clustering to group
our anomalies into organized segments that allow an analyst to 'skim' the output groups instead of looking at each row.

See zat/examples/anomaly\_detection.py for full code listing (code
simplified below)

```python
# Create a Pandas dataframe from a Zeek log
log_to_df = LogToDataFrame()
zeek_df = log_to_df.create_dataframe('/path/to/dns.log')

# Using Pandas we can easily and efficiently compute additional data metrics
zeek_df['query_length'] = zeek_df['query'].str.len()

# Use the zat DataframeToMatrix class
features = ['Z', 'rejected', 'proto', 'query', 'qclass_name', 'qtype_name', 'rcode_name', 'query_length']
to_matrix = dataframe_to_matrix.DataFrameToMatrix()
zeek_matrix = to_matrix.fit_transform(zeek_df[features])

# Train/fit and Predict anomalous instances using the Isolation Forest model
odd_clf = IsolationForest(contamination=0.35) # Marking 35% as odd
odd_clf.fit(zeek_matrix)

# Add clustering to our anomalies
zeek_df['cluster'] = KMeans(n_clusters=4).fit_predict(zeek_matrix)

# Now we create a new dataframe using the prediction from our classifier
odd_df = zeek_df[features+['cluster']][odd_clf.predict(zeek_matrix) == -1]

# Now group the dataframe by cluster
cluster_groups = zeek_df[features+['cluster']].groupby('cluster')

# Now print out the details for each cluster
print('<<< Outliers Detected! >>>')
for key, group in cluster_groups:
    print('\nCluster {:d}: {:d} observations'.format(key, len(group)))
    print(group.head())
```

**Example Output:** Run this example script on your Zeek dns.log\...

    <<< Outliers Detected! >>>

    Cluster 0: 4 observations
        Z rejected proto                                              query qclass_name qtype_name rcode_name  query_length  cluster
    53  0    False   udp  superlongcrazydnsqueryforanomalydetectionj.max...  C_INTERNET          A    NOERROR            54        0
    54  0    False   udp  xyzsuperlongcrazydnsqueryforanomalydetectionj....  C_INTERNET          A    NOERROR            57        0
    55  0    False   udp  abcsuperlongcrazydnsqueryforanomalydetectionj....  C_INTERNET          A    NOERROR            57        0
    56  0    False   udp  qrssuperlongcrazydnsqueryforanomalydetectionj....  C_INTERNET          A    NOERROR            57        0

    Cluster 1: 11 observations
        Z rejected proto query qclass_name qtype_name rcode_name  query_length  cluster
    39  0    False   udp     -           -          -          -             1        1
    40  0    False   udp     -           -          -          -             1        1
    41  0    False   udp     -           -          -          -             1        1
    42  0    False   udp     -           -          -          -             1        1
    43  0    False   udp     -           -          -          -             1        1

    Cluster 2: 6 observations
        Z rejected proto          query qclass_name qtype_name rcode_name  query_length  cluster
    61  0    False   tcp  j.maxmind.com  C_INTERNET          A    NOERROR            13        2
    62  0    False   tcp  j.maxmind.com  C_INTERNET          A    NOERROR            13        2
    63  0    False   tcp  j.maxmind.com  C_INTERNET          A    NOERROR            13        2
    64  0    False   tcp  j.maxmind.com  C_INTERNET          A    NOERROR            13        2
    65  0    False   tcp  j.maxmind.com  C_INTERNET          A    NOERROR            13        2

    Cluster 3: 4 observations
        Z rejected proto          query qclass_name qtype_name rcode_name  query_length  cluster
    57  1    False   udp  j.maxmind.com  C_INTERNET          A    NOERROR            13        3
    58  1    False   udp  j.maxmind.com  C_INTERNET          A    NOERROR            13        3
    59  1    False   udp  j.maxmind.com  C_INTERNET          A    NOERROR            13        3
    60  1    False   udp  j.maxmind.com  C_INTERNET          A    NOERROR            13        3

### Tor detection and port number count

See zat/examples/tor\_and\_port\_count.py for the code.

This example will go through ssl.log files and try to identify possible Tor traffic. This is done by using the well known pattern of the Issuer and Subject ID in the certificates. Please note that your Zeek installation will have to be configured to log these fields for this to work. Further info about how to do that can be found here: [SSL Log
Info](https://www.bro.org/sphinx/scripts/base/protocols/ssl/main.bro.html#type-SSL::Info)

**Example Output:** Run this example script on your Zeek ssl.log\...

    Possible Tor connection found
    From: 10.0.0.126 To: 82.96.35.7 Port: 443

The script will also keep a count of which destination ports that SSL
have been detected on. Something that might help with threat hunting
since you might find traffic on a port you definitely wasn't expecting
to be there.

**Example Output:** Run this example script on your Zeek ssl.log\...

    Port statistics
    443     513
    8443    173
    9997    21
    9001    20
    8080    2
    80      2
    5901    1
    9081    1
    447     1
