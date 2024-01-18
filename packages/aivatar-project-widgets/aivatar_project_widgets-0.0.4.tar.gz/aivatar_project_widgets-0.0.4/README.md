aivatar_project_widgets
=========

## Quick Start

```python
    from aivatar_project_widgets import AivProjectWindow

    def func(project_id, project_name, experiment):
        """ pass current project_id & experiment
        """
        if project_id < 0:
            print("invalid project")
            return
        # todo: show tools' window here
        print("current project_id: {}, name: {}, experiment: {}".format(project_id, project_name, experiment))

    # todo: get token from Login module
    project_window = AivProjectWindow(
                                      token, terminal_type, business_type,  # necessary
                                      parent_window=parent, on_confirm=func, is_test=False  # opt
                                      )

    if project_window.should_popup():
        project_window.popup()

    # get project info
    print(project_window.current_project_id)
    print(project_window.current_project_name)
    print(project_window.current_project_experiment)
```

## Advance

```python
    # view project items
    for item in project_window.project_items:
        print(item.project_id, item.project_name, item.experiment)

    # turn off on_confirm
    project_window.on_confirm = None

    # operate AivProjectAPI
    project_window.project_api
```

## Reference

[aivatar_project_api](https://git.woa.com/DCC_Client/Framework/aivatar_project_api)
