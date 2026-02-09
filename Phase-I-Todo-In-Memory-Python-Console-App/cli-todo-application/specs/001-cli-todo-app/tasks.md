# Tasks: CLI Todo App

**Feature Branch**: `001-cli-todo-app`
**Created**: 2025-12-28
**Spec**: specs/001-cli-todo-app/spec.md
**Plan**: specs/001-cli-todo-app/plan.md

## Implementation Strategy

The project will be implemented incrementally, prioritizing core user stories first. A Minimum Viable Product (MVP) will encompass the "Add a New Task" functionality (User Story 1), allowing for early user feedback and iterative development. Subsequent user stories will be integrated in priority order, with comprehensive testing at each stage.

## Phase 1: Setup

These tasks focus on initializing the project structure and development environment.

- [x] T001 Create project root directory structure: `src/`, `tests/`
- [x] T002 Initialize Python project (e.g., `pyproject.toml` or `requirements.txt`)
- [x] T003 Configure `pytest` for testing environment
- [x] T004 Create `src/models/`, `src/services/`, and `src/cli/` directories
- [x] T005 Create `tests/unit/` and `tests/integration/` directories

## Phase 2: Foundational

These tasks establish core components necessary for all user stories.

- [x] T006 Define `Task` entity with `description`, `status`, and `identifier` in `src/models/task.py`
- [x] T007 Implement an in-memory storage class (e.g., `TaskManager`) in `src/services/task_manager.py` to hold `Task` objects, ensuring an empty list on initialization.

## Phase 3: Interactive CLI Refactor & New Features

These tasks refactor the CLI to be interactive and implement new features (update, mark incomplete).

- [x] T008 [US1] Implement `add_task` method in `src/services/task_manager.py` (already done)
- [x] T009.1 [US1] Refactor `src/cli/main.py` for interactive mode, implementing `add` command.
- [x] T010 [US1] Add unit tests for `add_task` method in `tests/unit/test_task_manager.py` (already done)
- [x] T011 [US1] Add integration tests for `todo add` command in `tests/integration/test_cli.py` (already done, needs update for interactive)

- [x] T012 [US2] Implement `list_tasks` method in `src/services/task_manager.py` (already done)
- [x] T013.1 [US2] Implement `list` command in interactive CLI within `src/cli/main.py`.
- [x] T014 [US2] Add unit tests for `list_tasks` method in `tests/unit/test_task_manager.py` (already done)
- [x] T015 [US2] Add integration tests for `todo list` command in `tests/integration/test_cli.py` (already done, needs update for interactive)

- [x] T016 [US3] Implement `mark_task_complete` method in `src/services/task_manager.py` (already done)
- [x] T017.1 [US3] Implement `complete` command in interactive CLI within `src/cli/main.py`.
- [x] T018 [US3] Add unit tests for `mark_task_complete` method in `tests/unit/test_task_manager.py` (already done)
- [x] T019 [US3] Add integration tests for `todo complete` command in `tests/integration/test_cli.py` (already done, needs update for interactive)

- [x] T020 [US4] Implement `remove_task` method in `src/services/task_manager.py` (already done)
- [x] T021.1 [US4] Implement `remove` command in interactive CLI within `src/cli/main.py`.
- [x] T022 [US4] Add unit tests for `remove_task` method in `tests/unit/test_task_manager.py` (already done)
- [x] T023 [US4] Add integration tests for `todo remove` command in `tests/integration/test_cli.py` (already done, needs update for interactive)

- [ ] T027 [US5] Implement `update_task` method in `src/services/task_manager.py`. (Already done)
- [ ] T027.1 [US5] Implement `update` command in interactive CLI within `src/cli/main.py`.
- [ ] T028 [US6] Implement `mark_task_incomplete` method in `src/services/task_manager.py`. (Already done)
- [ ] T028.1 [US6] Implement `incomplete` command in interactive CLI within `src/cli/main.py`.

- [x] T029 Add unit tests for `update_task` method in `tests/unit/test_task_manager.py`.
- [x] T030 Add unit tests for `mark_task_incomplete` method in `tests/unit/test_task_manager.py`.
- [x] T031 Update integration tests in `tests/integration/test_cli.py` to test interactive CLI functionality.
- [x] T032 Update `README.md` to reflect interactive usage.

## Dependencies

- Phase 1 (Setup) is a prerequisite for all subsequent phases.
- Phase 2 (Foundational) is a prerequisite for all subsequent phases.
- Tasks T009.1, T013.1, T017.1, T021.1, T027.1, T028.1 depend on the `src/cli/main.py` refactoring.
- Test tasks (T029, T030, T031) depend on their respective implementation tasks.

## Parallel Execution Opportunities

- Tasks for implementing CLI commands (T009.1, T013.1, T017.1, T021.1, T027.1, T028.1) are largely independent of each other once `src/cli/main.py` is refactored for the interactive loop.
- Unit tests (T029, T030) can be developed in parallel with their corresponding service method implementations.

## Suggested MVP Scope

The MVP scope for the CLI Todo App is the core interactive loop with `add`, `list`, `complete`, and `remove` commands.

