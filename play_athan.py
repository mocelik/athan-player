#!/usr/bin/env python3

from datetime import datetime
from datetime import timedelta
from zoneinfo import ZoneInfo
from time import sleep
import geocoder
import pygame.mixer
import argparse

from adhanpy.calculation import CalculationMethod
from adhanpy.PrayerTimes import PrayerTimes


def print_prayer_times(when: datetime, prayer_times: PrayerTimes):
    format = "%H:%M"
    print(f"Prayer times for {when.strftime('%A %d %B %Y')}:")
    print(f"Fajr:    {prayer_times.fajr.astimezone().strftime(format)}")
    print(f"Sunrise: {prayer_times.sunrise.astimezone().strftime(format)}")
    print(f"Dhuhr:   {prayer_times.dhuhr.astimezone().strftime(format)}")
    print(f"Asr:     {prayer_times.asr.astimezone().strftime(format)}")
    print(f"Maghrib: {prayer_times.maghrib.astimezone().strftime(format)}")
    print(f"Isha:    {prayer_times.isha.astimezone().strftime(format)}")

def getNextPrayerTime(now: datetime = datetime.now()) -> datetime:
    now = now.astimezone()

    g = geocoder.ip('me')
    coordinates = (g.lat, g.lng)
    prayer_times = PrayerTimes(
        coordinates, now, CalculationMethod.NORTH_AMERICA
    )

    if now < prayer_times.fajr:
        return prayer_times.fajr

    if now < prayer_times.dhuhr:
        return prayer_times.dhuhr

    if now < prayer_times.asr:
        return prayer_times.asr

    if now < prayer_times.maghrib:
        return prayer_times.maghrib

    if now < prayer_times.isha:
        return prayer_times.isha

    next_day = now + timedelta(days=1)
    prayer_times = PrayerTimes(
        coordinates, next_day, CalculationMethod.NORTH_AMERICA
    )
    print("Next days prayer times: ")
    print_prayer_times(next_day, prayer_times)
    return prayer_times.fajr


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("athan_sound_file")
    args = parser.parse_args()

    pygame.init()
    pygame.mixer.init()
    athan_sound = pygame.mixer.Sound(args.athan_sound_file)
    athan_sound.set_volume(1.0)
 
    while True:
        now = datetime.now()
        next_prayer_time = getNextPrayerTime(now)

        print(f"Sleeping until {next_prayer_time.astimezone()}")
        sleep((next_prayer_time - now.astimezone()).seconds)
        athan_sound.play()
