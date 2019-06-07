IF NOT EXIST %UserProfile%\miniconda3\envs\pygame_projects_env (
	
	echo Please wait while the Conda Environment (in %UserProfile%\miniconda3\envs) is being updated ...
	call %UserProfile%\miniconda3\Scripts\activate.bat %UserProfile%\miniconda3 && %UserProfile%\miniconda3\Scripts\conda env create -f %~dp0\environment.yml
	
) ELSE (
	echo The Conda Environment already exists.
)