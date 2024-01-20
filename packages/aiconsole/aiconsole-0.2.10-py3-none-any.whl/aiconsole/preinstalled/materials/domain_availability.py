import subprocess


def is_domain_available(domain) -> bool:
    """
    Use this function to check whenever domain is free to register, or taken, do not use any other method of checking this.

    example use:
    ```python
    is_domain_available('example.com')
    ```
    """
    try:
        result = subprocess.run(["whois", domain], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout.lower()

        if "Domain Status: No Object Found" in result.stdout:
            return True

        if "No match for domain" in result.stdout:
            return True

        # Common indicators that a domain is taken:
        indicators = ["registrant", "creation date", "domain name:", "status:"]

        for indicator in indicators:
            if indicator in output:
                return False  # Domain is taken

        # If none of the indicators are found, it might be available
        return True
    except Exception as e:
        print(f"Error checking domain {domain}: {e}")
        return False  # Can't determine
