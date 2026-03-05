[gh-conf-ssh-keys]: https://docs.github.com/en/authentication/connecting-to-github-with-ssh
[gh-troubleshoot-ssh-keys-conf]: https://docs.github.com/authentication/troubleshooting-ssh
[claude-pricing]: https://claude.com/pricing
[claude-install]: https://claude.com/product/claude-code

![AI Coding Labb](resources/heading-image.png)

# Pre-requisites

- GitHub account, free suffices.
  - Remember to configure your [SSH Keys][gh-conf-ssh-keys] if you plan to clone locally the repo using SSH; you may refer to their [troubleshooting guide][gh-troubleshoot-ssh-keys-conf] if you face any issues.
- VS Code + Python extension, Pyright, etc.
- Your preferred terminal emulator (optional)
- Claude Subscription, _Free_ suffices. You can get one at [Claude Pricing][claude-pricing]

# Exercises and Setup

We'll go over two different exercises where we'll work together with Claude Code to perform programming tasks; the exercises can be carried out locally on your machine or in _GitHub Codespaces_.

# Getting Started

## Fork the Repository

You'll work on a copy of this repository (forked), to do so locate the the fork button found at the top of the repository page, along _Watch_ and _Star_.

![gh-code-toolbar](resources/gh-repo-toolbar.png)

1. Click the Fork button.
2. Make your user is selected in the _Owner_ drop-down.
3. Provide a name for the repository or leave as-is.

You may now browse to the new repository under your account.

## Get Sources

### Option 1 - Start Codespaces

Once you are in front page of your forked repository:

1. Click the _Code_ green button which will open up a palette.
2. Select _Codespaces_ and then click on the green button _Create Codespace on main_. 

![gh-repo-code](resources/gh-codespaces.png)

The above will open up a new tab where a new codepace will be bootstrapped, wait for it to finish whereat you should see an instance of an editor with the file tree on the left side.

### Option 2 - Clone the Repository

Once you are in front page of your forked repository:

1. Click on the _Code_ green button which will open a palette.
2. While on the _Local_ tab, _Clone_ using SSH; you may alternatively use the GitHub CLI if you already have set it up.

## Installing Claude Code

Naviaget to [Install Claude Code][claude-install] and select the option that suits your platform and workstation configuration.

### GitHub Codespaces

You may install the Claude Code extension via the Plugin Browser just as you'd do for the desktop version of Visual Studio Code; you may do this after you have boostrapped your codespace described in the following steps.

# Authenticating

Start Claude Code by:

- VS Code or Codespaces: if the tab isn't visible yet, hit _Ctrl+Shift+P_ to show the command palette, then Claude > Open in New Tab.
- Terminal emulator: first make sure you are positioned in the directory where you've cloned the repository, then run the command *claude*.




# Exercise #1 - Refactor the Asset Management Application

# Exercise #2 - Create an Application from Scratch
