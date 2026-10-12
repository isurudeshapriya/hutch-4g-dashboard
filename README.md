# Hutch 4G Dashboard on GitHub (step by step)

Your dashboard runs as a free website on **GitHub Pages**. The weekly Excel report is converted
automatically and every user sees the same data. Week W40 is already included.

## A. One-time setup (about 15 minutes)

1. **Create a GitHub account** at https://github.com/signup (skip if you have one).
2. Click **+ (top right) -> New repository**.
   - Name: `hutch-4g-dashboard`
   - Choose **Public** (free Pages works only on public repos; a private site needs a paid GitHub Team/Enterprise plan - see "Privacy" below)
   - Tick **Add a README file** -> **Create repository**.
3. **Unzip** this package on your computer. Make sure hidden files are visible (Windows: File Explorer -> View -> Show -> *Hidden items*) so you can see the `.github` folder.
4. In your repository click **Add file -> Upload files**. Drag **everything inside the unzipped folder** (`index.html`, `data`, `reports`, `scripts`, `.github`, ...) into the page. Wait until all files show, then click **Commit changes**.
   - If the `.github` folder did not upload: click **Add file -> Create new file**, type the name `.github/workflows/build.yml` (typing the `/` makes folders), open `workflow-build.yml.txt` from this package, copy all its text into the box, and click **Commit changes**.
5. Go to **Settings -> Pages**. Under **Build and deployment -> Source** choose **GitHub Actions**.
6. Go to **Settings -> Actions -> General**. At the bottom, **Workflow permissions** -> choose **Read and write permissions** -> **Save**.
7. Go to the **Actions** tab -> click **Build data and deploy** (left side) -> **Run workflow** -> **Run workflow**. Wait 2-4 minutes until the circle becomes a green tick.
8. Open **Settings -> Pages**. You will see **"Your site is live at https://YOUR-NAME.github.io/hutch-4g-dashboard/"**. That is your dashboard link - send it to your users.

## B. Every week: add the new report (2 minutes)

1. Name the Excel file with the **year and week**, for example `4G_Utilization_Report_2026_W41.xlsx`
   (the sheet must be called `Cells`, same layout as now).
2. Open your repository -> open the **reports** folder -> **Add file -> Upload files** -> drag the Excel file (you can drag several weeks at once) -> **Commit changes**.
   - GitHub's browser upload accepts files up to **25 MB**. If a file is bigger, use B2 below.
3. Wait about 3-5 minutes (watch the **Actions** tab for the green tick). Refresh the dashboard link (Ctrl+F5).
   The new week appears for **all users**, and the Trends and District pages include it automatically.
4. Old weeks are kept as small data files (about 0.8 MB each), so the history grows week by week.

### B2. Bigger files or no browser upload (optional)
Install Python, run `pip install pandas openpyxl`, then on your computer:
`python scripts/convert.py "C:\path\4G_Utilization_Report_2026_W41.xlsx"`
and upload the changed `data` folder to GitHub (Add file -> Upload files). Only small JSON files are uploaded.

## C. Good to know
- **Privacy:** a public repository and its website can be opened by anyone who has the link, and the data files can be downloaded. Network data is sensitive - get your company's approval first. For a private site use GitHub Team/Enterprise Cloud (Pages access control), or host the same folder on your company's web server.
- **Repository size:** each Excel upload stays in Git history (about 18 MB/week, roughly 1 GB per year). If that worries you, use option B2 so only the small JSON files are uploaded.
- **Delete / replace a week:** upload the same week's Excel again to replace it; to remove a week, delete `data/weeks/YYYY-Www.json` and its line in `data/manifest.json`.
- **Preview button:** "Preview an Excel file (not saved)" in the dashboard only shows a file on your own screen. Saving for everyone is done through the `reports` folder.
- **Same rules as before:** the congestion rules, band bandwidth, TB = GB / 1024, export to Excel, trends and district pages all work as in the earlier version.

## D. If something goes wrong
| Problem | What to do |
|---|---|
| Red cross in **Actions** | Click the run -> click the red step -> read the message. |
| "cannot detect the week" | Rename the file to include the year and week, e.g. `..._2026_W41.xlsx`. |
| "unexpected Cells layout" | The sheet must be named `Cells` with the same columns as the W40 report. |
| Error pushing / "permission denied" | Redo step A6 (Read and write permissions) and run the workflow again. |
| Site shows "cannot load data" | Open the **https://...github.io/...** link, not the downloaded `index.html`. |
| New week not visible | Wait for the green tick, then press Ctrl+F5. |
| Pages setting missing | Repository must be Public (free plan) - Settings -> Pages. |
