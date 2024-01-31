# Open AI Doc Project

Using Open AI generate Markdown documents of the entire project, then formulate an overall project summary. It uses Open AI and will charge your account depending how many files it needs to process. In general, the costs should be minimal, but they could go up depending on if you change settings, process a lot of files or re-run it many times, so please use discretion. This project was written on MacOS, so you may need to make adjustments for Windows or Linux.

- Copy the ".env.example" file to ".env" and add you Open AI API key.

- This is project is meant to be placed in your existing project to gather root and other project folders as specified.

- From the folder "openai_doc_project" run the generate_project_file_lists.py first to create the file paths and word count to be later processed by "generate_openai_summary.py"

- Once you have file to process, which could include the root of your project and other folders depending on what you include / exclude, update the "generate_openai_summary.py" prefix variable. That script is meant to run one project file set at a time, so I purposely didn't write it to loop over many project file sets, just one (which can include many files).