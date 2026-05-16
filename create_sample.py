"""Quick script to generate a sample contract as an image for testing."""
from PIL import Image, ImageDraw, ImageFont
import textwrap

CONTRACT = """
SOFTWARE AS A SERVICE AGREEMENT

This Software as a Service Agreement ("Agreement") is entered into as of January 15, 2026
("Effective Date"), by and between:

Provider: CloudTech Solutions Inc., a Delaware corporation ("Provider")
Client: Meridian Enterprises Ltd., a UK company ("Client")

1. SERVICES AND LICENSE
1.1 Provider grants Client a non-exclusive, non-transferable license to access and use
the CloudTech Enterprise Platform ("Service") during the Term.
1.2 Provider retains all intellectual property rights in the Service, including all
modifications, improvements, and derivative works, even those created based on Client feedback.

2. FEES AND PAYMENT
2.1 Client shall pay Provider $48,000 per year, billed monthly at $4,000 per month.
2.2 Late payments shall incur interest at 18% per annum, compounded monthly.
2.3 Provider may increase fees by up to 25% upon each annual renewal with 30 days notice.

3. TERM AND TERMINATION
3.1 This Agreement shall be effective for an initial term of 3 years ("Initial Term").
3.2 After the Initial Term, the Agreement automatically renews for successive 2-year periods
unless either party provides written notice of non-renewal at least 90 days prior.
3.3 Provider may terminate this Agreement immediately for any reason with 30 days notice.
3.4 Client may terminate only for material breach by Provider, after providing 60 days
written notice and opportunity to cure.

4. DATA AND PRIVACY
4.1 Client grants Provider a perpetual, irrevocable, worldwide license to use, modify,
and create derivative works from all data uploaded to the Service ("Client Data").
4.2 Provider may share anonymized Client Data with third parties for analytics and
research purposes without additional consent.

5. LIABILITY AND INDEMNIFICATION
5.1 Provider's total liability under this Agreement shall not exceed the fees paid by
Client in the 3 months preceding the claim.
5.2 Client shall indemnify, defend, and hold harmless Provider against any and all claims,
damages, losses, and expenses arising from Client's use of the Service, including
claims by third parties, without limitation.
5.3 IN NO EVENT SHALL PROVIDER BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL,
CONSEQUENTIAL, OR PUNITIVE DAMAGES.

6. NON-COMPETE AND NON-SOLICITATION
6.1 During the Term and for 3 years after termination, Client shall not directly or
indirectly develop, market, or sell any software product that competes with the Service.
6.2 Client shall not solicit or hire any Provider employee for 2 years after termination.

7. DISPUTE RESOLUTION
7.1 All disputes shall be resolved by binding arbitration in Wilmington, Delaware,
under the rules of the American Arbitration Association.
7.2 The prevailing party shall be entitled to recover its reasonable attorneys' fees.

8. GOVERNING LAW
This Agreement shall be governed by the laws of the State of Delaware.

IN WITNESS WHEREOF, the parties have executed this Agreement as of the Effective Date.

_________________________          _________________________
CloudTech Solutions Inc.           Meridian Enterprises Ltd.
"""

width, height = 1200, 2200
img = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(img)

try:
    font = ImageFont.truetype("arial.ttf", 18)
    font_bold = ImageFont.truetype("arialbd.ttf", 22)
except:
    font = ImageFont.load_default()
    font_bold = font

y = 40
for line in CONTRACT.strip().split("\n"):
    line = line.strip()
    if not line:
        y += 14
        continue
    is_heading = line.isupper() or line.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.")) and len(line) < 50
    f = font_bold if is_heading else font
    wrapped = textwrap.wrap(line, width=80)
    for wl in wrapped:
        draw.text((60, y), wl, fill="black", font=f)
        y += 26
    y += 4

img.save("sample_contract.png")
print("Created sample_contract.png")
