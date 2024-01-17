# Webex Troubleshooting Copilot

This repository contains the Copilot SDK for Webex Troubleshooting Copilot. Copilot is an AI programming assistant that helps developers with code suggestions and examples.

## Brief Introduction

Webex Troubleshooting Copilot is a powerful tool that assists developers in troubleshooting their Webex applications. It leverages machine learning to provide intelligent code suggestions and examples, making it easier and faster to resolve issues.

## Example of Using Copilot SDK

To use the Copilot SDK in your project, follow these steps:

1. Install the Copilot SDK package:
    ```bash
    pip install copilotsdk
    ```

2. Import the Copilot module into your code:
```
    import copilotsdk
```

3. Initialize the Copilot instnace:
    ```python
        async def _test_start(): 

            copilot = WebexCopilot("localhost")
            await copilot.start()

            await asyncio.wait_for(copilot.ready, timeout=100)


        asyncio.run(_test_start())
    ```

4. Call Anomaly Check:
    ```python
        report = await copilot.generate_anomaly_report("https://jira-eng-gpk2.cisco.com/jira/secure/attachment/891712/tst_video_only_retry_10-14_15-56-16_log-42.12.0.23935.zip")

    ```
The paramerter can local file (current_log.txt or last_run_current_log.txt) or a link to control hub or jira.

5. Do Deep Analysis
With the fast check result, you can continue to call generate_anomaly_deep_analysis_report for failure details:

    ```python
        report = await copilot.generate_anomaly_deep_analysis_report("7159edd516f0b33981d7be140cd114628b902f5866c806fcf3be79f10ac9de47","join meeting","callid-e80f6b25-519f-4ad6-a4ba-6aa4ccff34ff.txt")
    ```


## License

This project is licensed under the [MIT License](LICENSE).
