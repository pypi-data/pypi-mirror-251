from django.db import models

class Selinux(models.Model):
    hostname = models.CharField(max_length=128, primary_key=True)
    status = models.CharField(max_length=50)
    mount = models.CharField(max_length=50)
    rootdir = models.CharField(max_length=50)
    policyname = models.CharField(max_length=50)
    current_mode = models.CharField(max_length=50)
    configured_mode = models.CharField(max_length=50)
    mslstatus = models.CharField(max_length=50)
    memprotect = models.CharField(max_length=50)
    maxkernel = models.CharField(max_length=50)
    total = models.CharField(max_length=50)
    success = models.CharField(max_length=50)
    failed = models.CharField(max_length=50)
    sealerts = models.CharField(max_length=50)
    def __str__(self):
        return self.hostname
    
    class Meta:
        db_table = 'selinux'
        verbose_name = 'Selinux'
        verbose_name_plural = 'Selinux'
        ordering = ['hostname']
# the id must auto increment, otherwise the data will be overwritten


class SElinuxEvent(models.Model):
    digest = models.CharField(max_length=256, primary_key=True)
    hostname = models.CharField(max_length=128)
    event = models.CharField(max_length=1024)
    date = models.DateField()
    time = models.TimeField()
    serial_num = models.IntegerField()
    event_kind = models.CharField(max_length=256, blank=True, null=True)
    session = models.CharField(max_length=256, blank=True, null=True)
    subj_prime = models.CharField(max_length=256, blank=True, null=True)
    subj_sec = models.CharField(max_length=256, blank=True, null=True)
    subj_kind = models.CharField(max_length=256, blank=True, null=True)
    action = models.CharField(max_length=256, blank=True, null=True)
    result = models.CharField(max_length=256, blank=True, null=True)
    obj_prime = models.CharField(max_length=256, blank=True, null=True)
    obj_sec = models.CharField(max_length=256, blank=True, null=True)
    obj_kind = models.CharField(max_length=256, blank=True, null=True)
    how = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.digest
    
    class Meta:
        db_table = 'selinux_event'
        verbose_name = 'SElinuxEvent'
        verbose_name_plural = 'SElinuxEvent'
        ordering = ['date', 'time', 'hostname']


class Setroubleshoot(models.Model):
    digest = models.CharField(max_length=256, primary_key=True)
    sealert = models.CharField(max_length=1024)
    firstseen = models.DateField()
    lastseen = models.DateField()
    count = models.IntegerField()
    def __str__(self):
        return self.digest
    
    class Meta:
        db_table = 'setroubleshoot'
        verbose_name = 'Setroubleshoot'
        verbose_name_plural = 'Setroubleshoot'
        ordering = ['lastseen', 'sealert']

class SetroubleshootEntry(models.Model):
    CURSOR = models.CharField(max_length=255, primary_key=True)
    REALTIMETIMESTAMP = models.BigIntegerField()
    MONOTONICTIMESTAMP = models.BigIntegerField()
    BOOTID = models.CharField(max_length=255)
    PRIORITY = models.IntegerField()
    SYSLOGFACILITY = models.IntegerField()
    SYSLOGIDENTIFIER = models.CharField(max_length=255)
    TRANSPORT = models.CharField(max_length=255)
    PID = models.IntegerField()
    UID = models.IntegerField()
    GID = models.IntegerField()
    COMM = models.CharField(max_length=255)
    EXE = models.CharField(max_length=255)
    CMDLINE = models.TextField()
    CAPEFFECTIVE = models.CharField(max_length=255)
    SELINUXCONTEXT = models.CharField(max_length=255)
    SYSTEMDCGROUP = models.CharField(max_length=255)
    SYSTEMDUNIT = models.CharField(max_length=255)
    SYSTEMDSLICE = models.CharField(max_length=255)
    MACHINEID = models.CharField(max_length=255)
    HOSTNAME = models.CharField(max_length=255)
    CODEFILE = models.CharField(max_length=255)
    CODELINE = models.CharField(max_length=255)
    CODEFUNC = models.CharField(max_length=255)
    MESSAGEID = models.CharField(max_length=255)
    UNIT = models.CharField(max_length=255)
    MESSAGE = models.TextField()
    INVOCATIONID = models.CharField(max_length=255)
    SOURCEREALTIMETIMESTAMP = models.BigIntegerField()
    digest = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return f"SetroubleshootEntry - {self.CURSOR}"

    class Meta:
        verbose_name = 'Setroubleshoot Entry'
        verbose_name_plural = 'Setroubleshoot Entries'
# Hostname is foreign key
        
class message(models.Model):
    digest = models.CharField(max_length=128, primary_key=True)  
    lastseen = models.DateField(None, blank=True, null=True)
    count = models.IntegerField(null=True)
    message = models.CharField(max_length=1024)
    hostname = models.CharField(max_length=128)
    machineid = models.CharField(max_length=128)

    def __str__(self):
        return self.message
    class Meta:
        db_table = 'message'
        verbose_name = 'message'
        verbose_name_plural = 'messages'

class suggesting(models.Model):
    digest = models.CharField(max_length=128)
    solution = models.CharField(max_length=1024)
    sourcecontext = models.CharField(max_length=128)
    targetcontext = models.CharField(max_length=128)
    targetobjecs = models.CharField(max_length=1024)
    source = models.CharField(max_length=128)
    sourcepath = models.CharField(max_length=128)
    port = models.CharField(max_length=128)
    host = models.CharField(max_length=128)
    sourcerpmpackages = models.CharField(max_length=128)
    targetrpmpackages = models.CharField(max_length=128)
    selinuxpolicyrpm = models.CharField(max_length=128)
    policytype = models.CharField(max_length=128)
    enforcingmode = models.CharField(max_length=128)
    hostname = models.CharField(max_length=128)
    platform = models.CharField(max_length=512) 
    lastseen = models.DateField(None, blank=True, null=True)
    localid = models.CharField(max_length=128)
    rawauditmessages = models.CharField(max_length=1024)

    def __str__(self):
        return self.digest
    class Meta:
        db_table = 'suggesting'
        verbose_name = 'suggesting'
        verbose_name_plural = 'suggestings'






    

