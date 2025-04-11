brew install git-lfs
git lfs install
git lfs track "*.h5"
git rm --cached custom_model.h5
git push origin main


python -m spacy download en_core_web_sm