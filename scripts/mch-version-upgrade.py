import os, sys, json, re, pprint
from github import Github, UnknownObjectException, GithubException

if __name__ == "__main__":

    # Simple Parameter Loading
    source_version = os.getenv("source_version")
    dest_version = os.getenv("dest_version")
    prev_version = os.getenv("prev_version")
    product_prefix = os.getenv("product_prefix")
    mch_release_repo_source_branch = "master"
    github_token = os.getenv("GITHUB_TOKEN")
    mch_repo = "stolostron/multiclusterhub-operator"
    mce_repo = "stolostron/backplane-operator"
    mce_source_version = os.getenv("mce_source_version")
    mce_dest_version = os.getenv("mce_dest_version")
    
    # Initialize our GitHub Connection
    
    gh = Github(github_token)
    mch_repo = gh.get_repo(mch_repo)
    mce_repo = gh.get_repo(mce_repo)

    #file locations:
    loc1 = ".github/workflows" 
    loc2 = "hack/bundle-automation/config.yaml"
    loc3 = "hack/prereqs/oc.yaml"
    loc4 = "hack/scripts/dev-update-image-references.py" 
    loc5 = "hack/scripts/generate_images.py" 
    loc6 = "pkg/multiclusterengine/multiclusterengine.go" 
    loc7 = "pkg/version/version.go" 
    loc8 = "test/function_tests/utils/resources.go" 

    # Create a working branch
    dest_branch=f"add-{product_prefix}-{dest_version}" # Name of our working branch in release
    mch_source_br = mch_repo.get_branch(mch_release_repo_source_branch)
    mch_repo.create_git_ref(ref=f"refs/heads/{dest_branch}", sha=mch_source_br.commit.sha)


    #loc1 
    print(f"Working on updates for file 1/8")
    try:
        source_bundle_file = f"{loc1}/regenerate-bundles-{prev_version}.yml"
        dest_bundle_file = f"{loc1}/regenerate-bundles-{source_version}.yml"
        # Grab the contents of source_file and decode
        old_bundle = mch_repo.get_contents(source_bundle_file).decoded_content.decode("utf-8")
        # Replace references to source_version in source_file with dest_version.
        new_bundle = re.sub(prev_version, source_version, old_bundle)
        # Create a commit with our dest_file
        mch_repo.create_file(dest_bundle_file, f"Add operator bundles action for Github Actions in the {dest_version} release", new_bundle, branch=dest_branch)
        print(f"[SUCCESS] Successfully created a new action for Github Actions.")
    except UnknownObjectException as e:
        print(e)
        print(f"[SKIPPING] Issue finding file {loc1}")

    #loc2 - 
    print(f"Working on updates for file 2/8")
    try:
        source_file = f"{loc2}"
        dest_file = f"{loc2}"
        # Grab the contents of source_file and decode
        old_cf = mch_repo.get_contents(source_file) # returns a github.ContentFile.ContentFile object
        old_file = old_cf.decoded_content.decode("utf-8") #returns decoded ContentFile in utf-8
        old_blob_sha = old_cf.sha #gets sha
        spec = "branch:" #this is the spec line we are looking for ERIN this could cause problems

        # Replace references to source_version in source_config_file with dest_version.
        updated_file = re.sub(source_version, dest_version, old_file)
        old_regex = f"{source_version.split('.')[0]}\.{source_version.split('.')[1]}"
        new_regex = f"{dest_version.split('.')[0]}\.{dest_version.split('.')[1]}"
        new_file = updated_file.replace(old_regex, new_regex)
        # Create a commit with our dest_file
        mch_repo.update_file(dest_file, f"Update MCH files for the {dest_version} release", new_file, 
                                      old_blob_sha, branch=dest_branch)
        print(f"[SUCCESS] Successfully created file 8/8 for the {dest_version} release.")
    except UnknownObjectException as e:
        print(e)
        print(f"[SKIPPING] Issue finding file {loc2}.")

    #loc3
    print(f"Working on updates for file 3/8")
    try:
        source_file = f"{loc3}"
        dest_file = f"{loc3}"
        # Grab the contents of source_file and decode
        old_cf = mch_repo.get_contents(source_file) # returns a github.ContentFile.ContentFile object
        old_file = old_cf.decoded_content.decode("utf-8") #returns decoded ContentFile in utf-8
        old_blob_sha = old_cf.sha #gets sha
        spec = "branch:" #this is the spec line we are looking for ERIN this could cause problems

        # Replace references to source_version in source_config_file with dest_version.
        updated_file = re.sub(source_version, dest_version, old_file)
        old_regex = f"{source_version.split('.')[0]}\.{source_version.split('.')[1]}"
        new_regex = f"{dest_version.split('.')[0]}\.{dest_version.split('.')[1]}"
        new_file = updated_file.replace(old_regex, new_regex)
        # Create a commit with our dest_file
        mch_repo.update_file(dest_file, f"Update MCH files for the {dest_version} release", new_file, 
                                      old_blob_sha, branch=dest_branch)
        print(f"[SUCCESS] Successfully created file 8/8 for the {dest_version} release.")
    except UnknownObjectException as e:
        print(e)
        print(f"[SKIPPING] Issue finding file {loc3}.")

    #loc4
    print(f"Working on updates for file 4/8")
    try:
        source_file = f"{loc4}"
        dest_file = f"{loc4}"
        # Grab the contents of source_file and decode
        old_cf = mch_repo.get_contents(source_file) # returns a github.ContentFile.ContentFile object
        old_file = old_cf.decoded_content.decode("utf-8") #returns decoded ContentFile in utf-8
        old_blob_sha = old_cf.sha #gets sha
        spec = "branch:" #this is the spec line we are looking for ERIN this could cause problems

        # Replace references to source_version in source_config_file with dest_version.
        updated_file = re.sub(source_version, dest_version, old_file)
        old_regex = f"{source_version.split('.')[0]}\.{source_version.split('.')[1]}"
        new_regex = f"{dest_version.split('.')[0]}\.{dest_version.split('.')[1]}"
        new_file = updated_file.replace(old_regex, new_regex)
        # Create a commit with our dest_file
        mch_repo.update_file(dest_file, f"Update MCH files for the {dest_version} release", new_file, 
                                      old_blob_sha, branch=dest_branch)
        print(f"[SUCCESS] Successfully created file 8/8 for the {dest_version} release.")
    except UnknownObjectException as e:
        print(e)
        print(f"[SKIPPING] Issue finding file {loc4}.")

    #loc5
    print(f"Working on updates for file 5/8")
    try:
        source_file = f"{loc5}"
        dest_file = f"{loc5}"
        # Grab the contents of source_file and decode
        old_cf = mch_repo.get_contents(source_file) # returns a github.ContentFile.ContentFile object
        old_file = old_cf.decoded_content.decode("utf-8") #returns decoded ContentFile in utf-8
        old_blob_sha = old_cf.sha #gets sha
        spec = "branch:" #this is the spec line we are looking for ERIN this could cause problems

        # Replace references to source_version in source_config_file with dest_version.
        updated_file = re.sub(source_version, dest_version, old_file)
        old_regex = f"{source_version.split('.')[0]}\.{source_version.split('.')[1]}"
        new_regex = f"{dest_version.split('.')[0]}\.{dest_version.split('.')[1]}"
        new_file = updated_file.replace(old_regex, new_regex)
        # Create a commit with our dest_file
        mch_repo.update_file(dest_file, f"Update MCH files for the {dest_version} release", new_file, 
                                      old_blob_sha, branch=dest_branch)
        print(f"[SUCCESS] Successfully created file 8/8 for the {dest_version} release.")
    except UnknownObjectException as e:
        print(e)
        print(f"[SKIPPING] Issue finding file {loc5}.")

    #loc6
    print(f"Working on updates for file 6/8")
    try:
        source_file = f"{loc6}"
        dest_file = f"{loc6}"
        # Grab the contents of source_file and decode
        old_cf = mch_repo.get_contents(source_file) # returns a github.ContentFile.ContentFile object
        old_file = old_cf.decoded_content.decode("utf-8") #returns decoded ContentFile in utf-8
        old_blob_sha = old_cf.sha #gets sha
        spec = "branch:" #this is the spec line we are looking for ERIN this could cause problems

        # Replace references to source_version in source_config_file with dest_version.
        updated_file = re.sub(mce_source_version, mce_dest_version, old_file)
        old_regex = f"{mce_source_version.split('.')[0]}\.{mce_source_version.split('.')[1]}"
        new_regex = f"{mce_dest_version.split('.')[0]}\.{mce_dest_version.split('.')[1]}"
        new_file = updated_file.replace(old_regex, new_regex)
        # Create a commit with our dest_file
        mch_repo.update_file(dest_file, f"Update MCH files for the {dest_version} release", new_file, 
                                      old_blob_sha, branch=dest_branch)
        print(f"[SUCCESS] Successfully created file 8/8 for the {dest_version} release.")
    except UnknownObjectException as e:
        print(e)
        print(f"[SKIPPING] Issue finding file {loc6}.")

    #loc7
    print(f"Working on updates for file 7/8")
    try:
        source_file = f"{loc7}"
        dest_file = f"{loc7}"
        # Grab the contents of source_file and decode
        old_cf = mch_repo.get_contents(source_file) # returns a github.ContentFile.ContentFile object
        old_file = old_cf.decoded_content.decode("utf-8") #returns decoded ContentFile in utf-8
        old_blob_sha = old_cf.sha #gets sha
        spec = "branch:" #this is the spec line we are looking for ERIN this could cause problems

        # Replace references to source_version in source_config_file with dest_version.
        updated_file = re.sub(mce_source_version, mce_dest_version, old_file)
        old_regex = f"{mce_source_version.split('.')[0]}\.{mce_source_version.split('.')[1]}"
        new_regex = f"{mce_dest_version.split('.')[0]}\.{mce_dest_version.split('.')[1]}"
        new_file = updated_file.replace(old_regex, new_regex)
        # Create a commit with our dest_file
        mch_repo.update_file(dest_file, f"Update MCH files for the {dest_version} release", new_file, 
                                      old_blob_sha, branch=dest_branch)
        print(f"[SUCCESS] Successfully created file 8/8 for the {dest_version} release.")
    except UnknownObjectException as e:
        print(e)
        print(f"[SKIPPING] Issue finding file {loc7}.")

    #loc8
    print(f"Working on updates for file 8/8")
    try:
        source_file = f"{loc8}"
        dest_file = f"{loc8}"
        # Grab the contents of source_file and decode
        old_cf = mch_repo.get_contents(source_file) # returns a github.ContentFile.ContentFile object
        old_file = old_cf.decoded_content.decode("utf-8") #returns decoded ContentFile in utf-8
        old_blob_sha = old_cf.sha #gets sha
        spec = "branch:" #this is the spec line we are looking for ERIN this could cause problems

        # Replace references to source_version in source_config_file with dest_version.
        updated_file = re.sub(mce_source_version, mce_dest_version, old_file)
        old_regex = f"{mce_source_version.split('.')[0]}\.{mce_source_version.split('.')[1]}"
        new_regex = f"{mce_dest_version.split('.')[0]}\.{mce_dest_version.split('.')[1]}"
        new_file = updated_file.replace(old_regex, new_regex)
        # Create a commit with our dest_file
        mch_repo.update_file(dest_file, f"Update MCH files for the {dest_version} release", new_file, 
                                      old_blob_sha, branch=dest_branch)
        print(f"[SUCCESS] Successfully created file 8/8 for the {dest_version} release.")
    except UnknownObjectException as e:
        print(e)
        print(f"[SKIPPING] Issue finding file {loc8}.")



