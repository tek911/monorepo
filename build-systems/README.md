# Build Systems

This directory contains multiple coexisting build systems to test scanner handling of complex build environments.

## Subdirectories

### bazel-workspace/
Bazel monorepo build configuration with:
- WORKSPACE file with external dependencies
- Multiple BUILD files
- Custom rules and macros
- Remote execution configuration

### gradle-multi/
Multi-project Gradle build with:
- Root `build.gradle` with subproject dependencies
- Version conflicts between subprojects
- Custom plugins
- Composite builds
- Both Groovy and Kotlin DSL files

### maven-reactor/
Maven multi-module project with:
- Parent POM with dependency management
- Child modules overriding versions
- BOM imports
- Build profiles changing dependencies
- Plugin configurations with vulnerabilities

### mixed-legacy/
Nightmare legacy build combining:
- Ant `build.xml`
- GNU Make files
- Shell scripts calling other build tools
- Hardcoded absolute paths
- Platform-specific build logic

## Scanner Challenges

- Correctly parsing dependency declarations across build systems
- Understanding multi-module relationships
- Resolving version conflicts
- Handling dynamic/computed versions
- Understanding build profiles and configurations
- Detecting vulnerable plugins (not just dependencies)
