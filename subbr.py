import os
import concurrent.futures
import argparse
import os
os.system("clear")
print("=====================================")
print("           Sub_Domain Bruit     ")
print("         Scripted by 0xTr1cky         ")
print("=====================================")
GREEN = '\033[92m'
RESET = '\033[0m'
RED = '\033[91m'
def check_ping(host):
    response = os.system(f"ping -c 1 {host} > /dev/null 2>&1")
    return response == 0  # Return True if ping was successful (host is live)

def check_subdomain(subdomain, domain, output_file):
    full_domain = f"{subdomain}.{domain}"
    if check_ping(full_domain):
        with open(output_file, 'a') as save_file:
            save_file.write(full_domain + '\n')
        print(f"[ {RED}LIVE{RESET} ]:{GREEN}{full_domain}{RESET}")

def check_and_save_subdomains(domain, subdomains_file, output_file):
    with open(subdomains_file, 'r') as file:
        subdomains = file.readlines()

    subdomains = [sub.strip() for sub in subdomains]

    with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as executor:
        futures = [executor.submit(check_subdomain, sub, domain, output_file) for sub in subdomains]
        for future in concurrent.futures.as_completed(futures):
            pass  # Wait for all threads to complete

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Subdomain discovery tool")
    parser.add_argument("-d", "--domain", type=str, help="Single domain to check")
    parser.add_argument("-dl", "--domain_list", type=str, help="File containing a list of domains")
    parser.add_argument("-i", "--input", type=str, help="Input subdomains file")
    parser.add_argument("-o", "--output", type=str, help="Output file to save found subdomains")
    args = parser.parse_args()

    if not args.input or not args.output:
        print("Please provide input file (-i) and output file (-o)")
    elif args.domain and args.domain_list:
        print("Please provide either a single domain (-d) or a file containing a list of domains (-dl), not both.")
    elif not args.domain and not args.domain_list:
        print("Please provide either a single domain (-d) or a file containing a list of domains (-dl)")
    else:
        domains = []
        if args.domain_list:
            with open(args.domain_list, 'r') as domain_file:
                domains = domain_file.readlines()
            domains = [domain.strip() for domain in domains]

        if args.domain:
            domains.append(args.domain)

        for domain in domains:
            check_and_save_subdomains(domain, args.input, args.output)
