import os, sys, json, re, pprint
from github import Github, UnknownObjectException, GithubException

if __name__ == "__main__":

    # Simple Parameter Loading
    source_version = os.getenv("source_version")
    source_pipeline_branch = os.getenv("source_pipeline_branch")
    dest_version = os.getenv("dest_version")
    product_prefix = os.getenv("product_prefix")
    osci_release_repo = os.getenv("osci_release_repo")
    osci_release_repo_source_branch = os.getenv("osci_release_repo_source_branch") if os.getenv("osci_release_repo_source_branch") is not None else "master"
    pipeline_repo = os.getenv("pipeline_repo")
    github_token = os.getenv("GITHUB_TOKEN")

    # Initialize our GitHub Connection
    gh = Github(github_token)
    pipeline_repo = gh.get_repo(pipeline_repo)
    osci_release_repo = gh.get_repo(osci_release_repo)

    # Compile a list of respositories for which we need to update configurations
    #   using the pipeline repo as our source of truth
    snapshots = pipeline_repo.get_contents('snapshots', ref=source_pipeline_branch)
    # Filter out downstream snapshots and gitkeep and sort newest-to-oldest
    r = re.compile('manifest-([0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2})-[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}\.json')
    snapshots = list(filter(lambda s: r.search(s.name), snapshots))
    snapshots.sort(key=lambda s: s.name, reverse=True)
    # If there are no snapashots to parse, report that.
    if len(snapshots) < 1:
        print(f"We found no snapshots upon which to base our list of components. Please check your pipeline repo/branch and try again.")
        exit(1)
    # Grab the latest snapshot, extract a list of repos, and filter/collapse to unique
    components = list(set([c['git-repository'] for c in json.loads(snapshots[0].decoded_content)]))
    
    # Armed with our list of components, let's wittle down the list to those with configs in osci_release_repo
    for c in components:
        try:
            osci_release_repo.get_contents(f"ci-operator/config/{c}")
        except UnknownObjectException as e:
            # Alert and skip if we don't find a config
            print(f"Could not find config for component {c} with the following error:")
            print(e)
            components.remove(c)
            continue # If we already removed it - don't waste the api query!
        try:
            osci_release_repo.get_contents(f"ci-operator/jobs/{c}")
        except UnknownObjectException as e:
            # Alert and skip if we don't find a jobs entry
            print(f"Could not find jobs for component {c} with the following error:")
            print(e)
            components.remove(c)
    
    # Now that we have a list of only the to-be-modified components... modify them and draft a commit!
    components.sort()
    # Create a working branch
    dest_branch=f"add-{product_prefix}-{dest_version}" # Name of our working branch in release
    osci_source_br = osci_release_repo.get_branch(osci_release_repo_source_branch)
    osci_release_repo.create_git_ref(ref=f"refs/heads/{dest_branch}", sha=osci_source_br.commit.sha)
    for c in components:
        print(f"Working on updates for {c}")
        # Try to genneate a new config file if there is one for he previous release
        try:
            source_config_file = f"ci-operator/config/{c}/{c.replace('/', '-')}-{product_prefix}-{source_version}.yaml"
            dest_config_file = f"ci-operator/config/{c}/{c.replace('/', '-')}-{product_prefix}-{dest_version}.yaml"
            # Grab the contents of source_file and decode
            old_config = osci_release_repo.get_contents(source_config_file).decoded_content.decode("utf-8")
            # Replace references to source_version in source_config_file with dest_version.
            new_config = re.sub(source_version, dest_version, old_config)
            # Create a commit with our dest_file
            osci_release_repo.create_file(dest_config_file, f"Add config file for {c} for the {dest_version} release", new_config, branch=dest_branch)
            print(f"[SUCCESS] Successfully created a new config file for {c}.")
        except UnknownObjectException as e:
            print(e)
            print(f"[SKIPPING] No source_version-ed config file found for {c}.")
        # Try to generate a new jobs presubmit file if there is one for he previous release
        try:
            source_job_file = f"ci-operator/jobs/{c}/{c.replace('/', '-')}-{product_prefix}-{source_version}-presubmits.yaml"
            dest_job_file = f"ci-operator/jobs/{c}/{c.replace('/', '-')}-{product_prefix}-{dest_version}-presubmits.yaml"
            # Grab the contents of source_file and decode
            old_job = osci_release_repo.get_contents(source_job_file).decoded_content.decode("utf-8")
            # Replace references to source_version in source_config_file with dest_version.
            updated_job = re.sub(source_version, dest_version, old_job)
            old_regex = f"{source_version.split('.')[0]}\.{source_version.split('.')[1]}"
            new_regex = f"{dest_version.split('.')[0]}\.{dest_version.split('.')[1]}"
            new_job = updated_job.replace(old_regex, new_regex)
            # Create a commit with our dest_file
            osci_release_repo.create_file(dest_job_file, f"Add job presubmit file for {c} for the {dest_version} release", new_job, branch=dest_branch)
            print(f"[SUCCESS] Successfully created a new job file for {c}.")
        except UnknownObjectException as e:
            print(e)
            print(f"[SKIPPING] No source_version-ed job presumbit file found for {c}.")
        # Try to generate a new jobs postsubmit file if there is one for he previous release
        try:
            source_job_file = f"ci-operator/jobs/{c}/{c.replace('/', '-')}-{product_prefix}-{source_version}-postsubmits.yaml"
            dest_job_file = f"ci-operator/jobs/{c}/{c.replace('/', '-')}-{product_prefix}-{dest_version}-postsubmits.yaml"
            # Grab the contents of source_file and decode
            old_job = osci_release_repo.get_contents(source_job_file).decoded_content.decode("utf-8")
            # Replace references to source_version in source_config_file with dest_version.
            updated_job = re.sub(source_version, dest_version, old_job)
            old_regex = f"{source_version.split('.')[0]}\.{source_version.split('.')[1]}"
            new_regex = f"{dest_version.split('.')[0]}\.{dest_version.split('.')[1]}"
            new_job = updated_job.replace(old_regex, new_regex)
            # Create a commit with our dest_file
            osci_release_repo.create_file(dest_job_file, f"Add job postsubmit file for {c} for the {dest_version} release", new_job, branch=dest_branch)
            print(f"[SUCCESS] Successfully created a new job postsubmit file for {c}.")
        except UnknownObjectException as e:
            print(e)
            print(f"[SKIPPING] No source_version-ed job file found for {c}.")
        
    # Try to generate a new top level prow config
    try:
        source_job_file = f"core-services/prow/02_config/_plugins.yaml"
        dest_job_file = f"core-services/prow/02_config/_plugins.yaml"
        # Grab the contents of source_file and decode
        old_config_cf = osci_release_repo.get_contents(source_job_file) # returns a github.ContentFile.ContentFile object
        old_config = old_config_cf.decoded_content.decode("utf-8")
        old_config_blob_sha = old_config_cf.sha
        # Find matching section to update
        jobStart = f"ci-operator/jobs/stolostron/**/*-{product_prefix}-{source_version}*.yaml:"
        reg_jobStart = f"ci-operator/jobs/stolostron/\*\*/\*-{product_prefix}-{source_version}\*\.yaml:"
        configStart = f"ci-operator/config/stolostron/**/*-{product_prefix}-{source_version}*.yaml:"
        reg_configStart = f"ci-operator/config/stolostron/\*\*/\*-{product_prefix}-{source_version}\*\.yaml:"
        End = "name:"
        # Do a regex search on the job config and replace references to source_version with dest_version.
        match1 = re.search(rf'\n(\s+{reg_jobStart}[\s\S]*?.*{End}.*\n)', old_config, re.M)
        # Split config on matching config section and insert replaced config
        insertion1 = re.sub(source_version, dest_version, match1.group(1))
        split1 = old_config.find(jobStart)+len(match1.group(1))
        mid_config = old_config[:split1] + insertion1.lstrip() + f"    {old_config[split1:]}"
        # Repeat the above 4 lines with the config section
        match2 = re.search(rf'\n(\s+{reg_configStart}[\s\S]*?.*{End}.*\n)', mid_config, re.M)
        split2 = mid_config.find(configStart)+len(match2.group(1))
        insertion2 = re.sub(source_version, dest_version, match2.group(1))
        new_config = mid_config[:split2] + insertion2.lstrip() + f"    {mid_config[split2:]}"
        # Create a commit with our dest_file
        osci_release_repo.update_file(dest_job_file, f"Add a top-level prow config file for the CI Operator for the {dest_version} release", new_config, 
                                      old_config_blob_sha, branch=dest_branch)
        print(f"[SUCCESS] Successfully created a top-level prow config file for the CI Operator for the {dest_version} release.")
    except UnknownObjectException as e:
        print(e)
        print(f"Failed to generate a top-level prow config file for the CI Operator for the {dest_version} release! Exiting!")
        exit(1)

    # Our work is done!
