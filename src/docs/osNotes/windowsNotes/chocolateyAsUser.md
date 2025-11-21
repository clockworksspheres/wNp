(AI generated, from search.brave.com) 

Yes, you can run Chocolatey as a non-administrator user, but it requires specific configuration to allow this functionality safely and securely.

For non-admin users to install software via Chocolatey without elevated privileges, the Chocolatey Agent Service must be installed and configured. This service runs under a local administrator account (by default, `ChocolateyLocalAdmin`) and handles package installations on behalf of non-admin users. To enable this, you can install the Chocolatey Agent and configure it with the following commands:

**NOTE:** chocolatey-agent is only available with the business addition of chocolatey.

```
choco install chocolatey-agent -y
choco feature disable --name=showNonElevatedWarnings
choco feature enable --name=useBackgroundService
choco feature enable --name=useBackgroundServiceWithNonAdministratorsOnly
```

If certain packages require user interaction during installation, you can also enable interactive mode:

```
choco feature enable --name=useBackgroundServiceInteractively
```

Additionally, you can install Chocolatey GUI for a user-friendly interface:

```
choco install chocolateygui -y
```

To ensure non-admin users only access approved packages, you can restrict access to specific sources. For example, you can disable the public Chocolatey community repository:

```
choco source disable -n=chocolatey
```

You can also configure internal repositories to be used with the agent service, such as:

```
choco source add --name=choco-1 http://choco-1 --allow-self-service
```

Once configured, non-admin users can use Chocolatey GUI to install, update, or uninstall packages from approved sources without needing administrator credentials. The Chocolatey Agent Service manages the actual installation process under an elevated context, while the user interface remains accessible to non-admin users.

Alternatively, for a simpler setup, you can use portable packages that do not require installation with administrative rights. These can be installed to a user-specific directory using the `choco install` command with the `--install-directory` option, allowing users to manage their own software without system-wide changes.

AI-generated answer. Please verify critical facts.

Copy

Elaborate

Share

![🌐](https://imgs.search.brave.com/xqCzHEP9SFw5ydCgnQM5gqVWXVuHSmzhaN3u34vnnZ0/rs:fit:32:32:1:0/g:ce/aHR0cDovL2Zhdmlj/b25zLnNlYXJjaC5i/cmF2ZS5jb20vaWNv/bnMvMDBkNmU5ZjMx/MmI1ZDcwNDIwNDVm/YWVmOTZlMmVkMGY5/MzNiNzgzODA2ZTRh/ZDMyMDZiYzEyY2Y4/NmEwZjgyNC9jb3J5/a25veC5kZXYv)

![🌐](https://imgs.search.brave.com/0v1O2-ho1d7t8A-Jb0nY4gk_EaLf69pRZOM4o6k3IK8/rs:fit:32:32:1:0/g:ce/aHR0cDovL2Zhdmlj/b25zLnNlYXJjaC5i/cmF2ZS5jb20vaWNv/bnMvMGIwNzE4Mzg0/MWZiYjc5NjI3OWI2/NTk2YjA3YWMzYmUw/ZWM0N2E4YmNjNGZj/YTVlOTljODlkYTFk/MGRlY2ZjYy9ibG9n/Lmlwc3dpdGNoLmNv/bS8)

![🌐](https://imgs.search.brave.com/U-eHNCapRHVNWWCVPPMTIvOofZULh0_A_FQKe8xTE4I/rs:fit:32:32:1:0/g:ce/aHR0cDovL2Zhdmlj/b25zLnNlYXJjaC5i/cmF2ZS5jb20vaWNv/bnMvN2ZiNTU0M2Nj/MTFhZjRiYWViZDlk/MjJiMjBjMzFjMDRk/Y2IzYWI0MGI0MjVk/OGY5NzQzOGQ5NzQ5/NWJhMWI0NC93d3cu/cmVkZGl0LmNvbS8)

![🌐](https://imgs.search.brave.com/gKbhnTRH7wNr_KOo2GAEyeYNqp2nQfTVh00ibIXMD-w/rs:fit:32:32:1:0/g:ce/aHR0cDovL2Zhdmlj/b25zLnNlYXJjaC5i/cmF2ZS5jb20vaWNv/bnMvYTAwYjk1ODlm/MTdkYzZlZDhmODA5/NTA2M2IyYjI4MjM1/NjEwNTgxZjViOGJm/NTA2NDNjYjJjMTJh/MDc0OTNlMS9kb2Nz/LmNob2NvbGF0ZXku/b3JnLw)

+