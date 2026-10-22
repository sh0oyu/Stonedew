# Cloud development

Each task already has an isolated checkout. Use `/workspace/Stonedew`; do not create a Git worktree unless explicitly requested. Preserve user changes.

```sh
source /workspace/.stonedew-env/activate.sh
cd /workspace/Stonedew
./gradlew --no-daemon build
```

The retained environment includes a Java 21 JDK, dependency caches, and Gradle 9.2.1. `activate.sh` refreshes wrapper proxy routing from current instance variables without storing proxy authentication. Gradle's init script uses the system Java CA store; TLS and distribution checksums stay enabled. These machine-specific files are outside the project and must not be committed.

For a client on a machine without a desktop:

```sh
source /workspace/.stonedew-env/activate.sh
cd /workspace/Stonedew
export DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 ALSOFT_DRIVERS=null
bash tools/start_cloud_display.sh
./gradlew --no-daemon runClient
```

`start_cloud_display.sh` reuses a working display or starts Xvfb with TCP listening disabled. The cloud installer supplies Xvfb under `/workspace/.stonedew-env/xvfb`. Mesa software rendering is used; audio output is disabled for the cloud smoke check. The helper does not provide a browser preview. Run the client locally for normal playtesting and sound.

Processes do not survive environment publication. Restart the display/client as needed. No server is needed for editing/building. The development client supports local singleplayer development; online authentication/multiplayer have not been validated, and the development client's session-service warnings do not establish missing project credentials.

Build resources are limited to two Gradle workers and a 2 GiB Gradle heap. Initial Minecraft preparation is expensive; subsequent builds reuse the cache. Do not repeatedly delete caches or run `clean` without a reason.
