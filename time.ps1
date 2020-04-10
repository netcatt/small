$time = Invoke-RestMethod -Uri http://worldtimeapi.org/api/ip

$timezones = Get-TimeZone -ListAvailable

# there is no global standard in names of timezones nor a unique id of them
# worldtimeapi always has city name in last part of timezone field
# microsoft has city names in display name
# therefore current solution is to match those names based on city 
foreach ($timezone in $timezones) {
    if ($timezone.DisplayName.ToString() -match $time.timezone.Split("/")[-1]) {
        $current_zone = $timezone
        break
    }
}

if (!$current_zone) {throw "Could'nt find time zone. exiting."}


Set-TimeZone -Name $current_zone.StandardName

Set-Date -Date (Get-Date -Date $time.datetime)