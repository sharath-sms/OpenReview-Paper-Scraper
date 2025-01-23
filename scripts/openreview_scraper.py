import openreview
import pandas as pd



client = openreview.api.OpenReviewClient(
    baseurl='https://api2.openreview.net',
    username="###", # replace with your username
    password="###" # replace with your password
)


conference_name="ICML"
year="2024"
country_code="IN"
country_domain=".in"


accepted_submissions = client.get_all_notes(content={'venueid': f"{conference_name}.cc/{year}/Conference"})

submission_numbers = set()
submission_titles = set()
for submission in accepted_submissions:
    author_profiles = openreview.tools.get_profiles(
        client, submission.content['authorids'].get('value', [])
    )
    for author_profile in author_profiles:
        if author_profile.content.get('history', [{}]):
            institution = author_profile.content.get('history', [{}])[0].get('institution', {})
            if institution.get('country') == country_code or institution.get('domain', "").endswith(country_domain):
                submission_numbers.add(submission.number)
                submission_titles.add(submission.content["title"]["value"])
                print(submission.content["title"]["value"])


papers_df = pd.DataFrame({"id":list(set(submission_numbers)), "title":list(set(submission_titles))})
papers_df.to_csv(f"{conference_name}_{year}.csv", index=False)