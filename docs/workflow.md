# Git Workflow 
the goal of this document is to provide a suggested workflow for contribuiting to the project. 

1. **Create a feature branch**:
Start from main, and create a new branch named with the feature you're working on. 
```
git checkout -b <feature_name>
```
2. **Commit to the branch frequently**: It's good to commit frequently to keep track of what you're working on.
```
#First commit 
git add .
git commit -m"my commit msg"
git push --set-upstream origin <feature_name>
```
3. **Test**:
Once done test your code (using pytest) Ex. test_feature.py 
```
class TestFeature():
 
    def test_some_function(self):
        """
        example test 
        """
        
        assert func_output = expected_output 
```
4. **Run pylint (appease Jason)**:
Pylint give's you style suggestions and gives your code a 0-10 score.
```
Running pylint examples 

pylint feature.py
pylint src
pylint src/feature.py 

```
5. **Merge**:
Once code is tested, and checked for good syle merge to main
```
git checkout main 
git merge <feature_name>
```
6. **Delete**:
Delete the branch once no longer needed.
```
git branch -d <feature_name>
```

## Pros:
- **Frequent Merging:** Minimizes integration issues by ensuring that changes work together early.
- **Feature Branches & Frequent Commits:** Keeps the team updated on each other's work, making collaboration easier.
- **Early Bug Detection:** Regular integration helps catch bugs sooner rather than later.
