import time
import query_builder

def run(test: str = "generic"):
    print(f"Running test: {test}")
    generic_test_cases="""Are all SCCM clients reporting healthy status?
    Which clients have not communicated with the SCCM server recently?
    Do we have an up-to-date inventory of all hardware assets?
    Are there any unauthorized software applications installed on client devices?
    Are all critical applications deployed successfully to the intended devices?
    Are there any application deployment failures that need attention?
    Are all devices compliant with the organization's security policies?
    Which devices are non-compliant and why?
    Is content distribution to distribution points successful?
    Are there any packages that have not been successfully distributed?
    Are all devices correctly assigned to their respective collections?
    Are there any collections that need to be updated or re-evaluated?
    Are all network boundaries and boundary groups correctly configured?
    Are there any clients that are not associated with any boundary group?
    Are all critical and security updates deployed and installed on all devices?
    Are there any devices that have failed to install recent updates?
    Are all task sequences for OS deployment executing successfully?
    Are there any devices that failed during the OSD process?
    Are all Endpoint Protection clients up-to-date and reporting healthy status?
    Are there any recent malware detection events that need investigation?
    Are user-device affinities correctly configured?
    Are there any devices without assigned primary users?
    Are power management policies being enforced on all devices?
    Are there any devices that are not compliant with power management settings?
    Is remote control functionality working for all client devices?
    Are there any devices that are not allowing remote control?
    Are software metering rules correctly configured and capturing data?
    Are there any applications with unexpected usage patterns?
    Are all scheduled reports generating and distributing correctly?
    Are there any reports that need to be updated or created for new requirements?
    Are all SCCM roles and permissions correctly assigned?
    Are there any users with unnecessary administrative privileges?
    Are regular backups of the SCCM database being performed?
    Is there a tested recovery plan in place for SCCM?
    Are all critical alerts and notifications being generated and reviewed?
    Are there any recurring alerts that need to be addressed?
    Are NAP policies correctly configured and enforced?
    Are there any devices that are not compliant with NAP policies?
    Are all patch deployments successfully reaching and installing on all devices?
    Are there any devices that are missing critical patches?
    Are all software updates synchronized and available for deployment?
    Are there any software updates that are not being deployed successfully?"""

    specific_test_cases="""Are all SCCM clients reporting a "Healthy" status in the last 24 hours?
    Which clients have not communicated with the SCCM server in the past 7 days?
    Do we have an up-to-date inventory of all hardware assets, including CPU, RAM, and disk space?
    Are there any unauthorized software applications installed on client devices that were not approved by IT?
    Are all critical applications, such as Microsoft Office and Antivirus, deployed successfully to the intended devices?
    Are there any application deployment failures in the last week that need attention?
    Are all devices compliant with the organization's security policies, including antivirus status and encryption?
    Which devices are non-compliant with the latest security patch and why?
    Is content distribution to all distribution points successful for the latest software update package?
    Are there any packages that have not been successfully distributed to at least 90% of the distribution points?
    Are all devices correctly assigned to their respective collections based on department and location?
    Are there any collections that have not been updated or re-evaluated in the past month?
    Are all network boundaries and boundary groups correctly configured to include all subnets?
    Are there any clients that are not associated with any boundary group and hence not receiving updates?
    Are all critical and security updates deployed and installed on all devices within the last patch cycle?
    Are there any devices that have failed to install the latest Windows 10 cumulative update?
    Are all task sequences for Windows 10 deployment executing successfully without any errors?
    Are there any devices that failed during the OSD process due to driver issues?
    Are all Endpoint Protection clients up-to-date and reporting a "Healthy" status in the Endpoint Protection dashboard?
    Are there any recent malware detection events that have not been resolved?
    Are user-device affinities correctly configured for all users working remotely?
    Are there any devices without assigned primary users that have been inactive for over 30 days?
    Are power management policies being enforced on all devices, specifically during non-business hours?
    Are there any devices that are not compliant with power management settings and remain powered on 24/7?
    Is remote control functionality working for all client devices within the IT support team?
    Are there any devices that are not allowing remote control due to firewall or configuration issues?
    Are software metering rules correctly configured and capturing data for all licensed applications?
    Are there any applications with unexpected usage patterns, such as high usage of non-business software?
    Are all scheduled reports generating and distributing correctly to the IT management team?
    Are there any reports that need to be updated or created for new compliance requirements?
    Are all SCCM roles and permissions correctly assigned, especially for administrative accounts?
    Are there any users with unnecessary administrative privileges that need to be reviewed?
    Are regular backups of the SCCM database being performed without errors?
    Is there a tested recovery plan in place for SCCM that includes both database and site recovery?
    Are all critical alerts and notifications being generated and reviewed by the IT operations team?
    Are there any recurring alerts that need to be addressed to prevent future incidents?
    Are NAP (Network Access Protection) policies correctly configured and enforced across all devices?
    Are there any devices that are not compliant with NAP policies and are being quarantined?
    Are all patch deployments successfully reaching and installing on all devices within the compliance deadline?
    Are there any devices that are missing critical patches and have not reported in the last 7 days?"""

    if test == "generic":
        test_cases=generic_test_cases.splitlines()
    else:
        test_cases=specific_test_cases.splitlines()

    for test in test_cases:
        query_builder.execute(test)
        time.sleep(3)

run("specific")
