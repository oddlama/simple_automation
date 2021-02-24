from simple_automation.exceptions import LogicError, MessageError, RemoteExecError
    Stringifies a given integer mode as an octal string (e.g. 493 → "755").
        A tuple of (file_type, str_octal_mode, owner, group), where file_type is one of ["file", "directory", "link", "other"]
    stat = context.remote_exec(["python", "-c", 'import os, sys, stat; s = os.lstat(sys.argv[1]); ft = "link" if stat.S_ISLNK(s.st_mode) else "file" if stat.S_ISREG(s.st_mode) else "directory" if stat.S_ISDIR(s.st_mode) else "other"; print(f"{ft};{stat.S_IMODE(s.st_mode)};{s.st_uid};{s.st_gid}")', path])
        mode, owner, group = resolve_mode_owner_group(context, int(mode), owner, group, None)
        elif cur_ft == "file":
            raise MessageError(f"Cannot create file on remote: Path already exists and is not a file (type is '{cur_ft}')")
        if cur_ft == "file":
                context.remote_exec(["sh", "-c", f"cat > \"$(echo '{dst_base64}' | base64 -d)\""], checked=True, input=content)