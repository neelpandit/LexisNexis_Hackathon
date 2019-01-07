import json
import requests

headers={
    "x-api-key":"x2YtaaayGv9lUXISFzRXU1TV3Ybzj04L6PzCoqNi",
    "Content-Type":"application/json"
}
payload={
    "data":"[4:41 PM, 10/12/2018] Shwetha: Rule 9019. Compromise and Arbitration(a) Compromise. On motion by the trustee and after notice and a hearing, the court may approve a compromise or settlement. Notice shall be given to creditors, the United States trustee, the debtor, and indenture trustees as provided in Rule 2002 and to any other entity as the court may direct.(b) Authority To Compromise or Settle Controversies Within Classes. After a hearing on such notice as the court may direct, the court may fix a class or classes of controversies and authorize the trustee to compromise or settle controversies within such class or classes without further hearing or notice."
           "(c) Arbitration. On stipulation of the parties to any controversy affecting the estate the court may authorize the matter to be submitted to final and binding arbitration."
           "Notes (As amended Mar. 30, 1987, eff. Aug. 1, 1987; Apr. 30, 1991, eff. Aug. 1, 1991; Apr. 22, 1993, eff. Aug. 1, 1993.)"
           "Notes of Advisory Committee on Rules—1983 Subdivisions (a) and (c) of this rule are essentially the same as the provisions of former Bankruptcy Rule 919 and subdivision (b) is the same as former Rule 8–514(b), which was applicable to railroad reorganizations. Subdivision (b) permits the court to deal efficiently with a case in which there may be a large number of settlements."\
           "Subdivision (a) is amended to conform to the language of §102(1) of the Code. Other amendments are stylistic and make no substantive change."
           "Notes of Advisory Committee on Rules—1991 Amendment This rule is amended to enable the United States trustee to object or otherwise be heard in connection with a proposed compromise or settlement and otherwise to monitor the progress of the case."
           "Notes of Advisory Committee on Rules—1993 Amendment"
    }

response=requests.post("https://23nt6yrife.execute-api.us-east-1.amazonaws.com/dev/ilabs-concept-extractor",data=json.dumps(payload),headers=headers)
print(json.dumps(response.json(),indent=4))