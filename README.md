# jartup

Small Python script that scaffolds a Maven Java project with folder structure, `pom.xml`, Maven Wrapper, optionally Git and Docker. Built this because I switched from IntelliJ to Neovim and missed the automatic project generation. No external dependencies, just the Python standard library.

## What it does

`jartup` sets up a ready-to-go Maven project:

- Standard folder structure (`src/main/java`, `src/test/java`, `src/main/resources`) based on the group ID
- `pom.xml` with group ID, artifact ID, and a Maven Jar Plugin configured to build a directly runnable JAR
- `Main.java`
- Maven Wrapper (`mvnw`/`mvnw.cmd`), so nobody needs Maven installed globally
- optional: Git repo (`--git`)
- optional: Dockerfile + docker-compose + .dockerignore (`--docker`)

Everything runs offline, no need for `mvn` itself to be installed (except once, to build the wrapper templates - see below).

## Installation

Clone the repo:

```bash
git clone https://github.com/axhislmc/jartup.git
cd jartup/
```

Make it executable and available globally:

```bash
chmod +x jartup.py
mkdir -p ~/.local/bin
ln -s "$PWD/jartup.py" ~/.local/bin/jartup
```

If `~/.local/bin` isn't in your `$PATH` yet, add this to your `.zshrc`/`.bashrc`:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

After that, `jartup` should be callable from anywhere in the terminal.

## Usage

```bash
jartup <group> <name> [options]
```

**Example:**

```bash
jartup com.axhislmc my-project -g -d -m
```

Creates a folder `my-project/` with package `com.axhislmc`, a Maven build, an initialized Git repo, and Docker setup.

### Arguments

| Argument | Description |
|---|---|
| `group` | Group ID, e.g. `com.axhislmc` - determines the package path |
| `name` | Project name - becomes the folder name and artifact ID |

### Options

| Flag | Short | Description |
|---|---|---|
| `--maven` | `-m` | Set up Maven Wrapper and `pom.xml` |
| `--git` | `-g` | Initialize Git repo, add `.gitignore` + `README.md` |
| `--docker` | `-d` | Add Dockerfile, docker-compose.yml, .dockerignore (automatically enables `--maven`) |
| `--force` | | Overwrites an existing folder with the same name (the old project is briefly backed up and restored on failure) |

Without any flags you just get the plain folder structure with `Main.java`.

## Build structure
 
What `jartup com.axhislmc my-project -g -d -m` actually generates:
 
```
my-project
├── docker-compose.yml
├── Dockerfile
├── .dockerignore
├── .git
├── .gitignore
├── .mvn
│   └── wrapper
│       └── maven-wrapper.properties
├── mvnw
├── mvnw.cmd
├── pom.xml
├── README.md
└── src
    ├── main
    │   ├── java
    │   │   └── com
    │   │       └── axhislmc
    │   │           └── Main.java
    │   └── resources
    └── test
        └── java
            └── com
                └── axhislmc
```

## Repo structure

```
jartup/
├── jartup.py
└── templates/
    ├── .dockerignore
    ├── .gitignore
    ├── .mvn/
    ├── Dockerfile
    ├── Main.java.tmpl
    ├── README.md.tmpl
    ├── docker-compose.yml.tmpl
    ├── mvnw
    ├── mvnw.cmd
    └── pom.xml.tmpl
```

Files with the `.tmpl` extension contain placeholders (`${group}`, `${name}`) that get replaced when generating a project. Everything else gets copied as-is.

The Maven Wrapper in `templates/` was generated once with `mvn wrapper:wrapper` and just sits there as a static template - if a newer wrapper version is ever needed, regenerate it and swap the files.

## Why no Gradle

I just don't like it. Maven works fine for me.
