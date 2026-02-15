#!/usr/bin/env python3

from datetime import datetime
from datetime import timedelta
from zoneinfo import ZoneInfo
from time import sleep
import geocoder
import os
import warnings
import contextlib
import argparse

# Hide pygame support prompt and suppress import-time runtime warnings
# Must be set before importing pygame submodules that print on import
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame.mixer

from adhanpy.calculation import CalculationMethod
from adhanpy.PrayerTimes import PrayerTimes

class PrayerTimeCalculator:
    def __init__(self,  coordinates: tuple[float, float]):
        self.coordinates = coordinates
        self.print_prayer_times(self.now(), PrayerTimes(coordinates, self.now(), CalculationMethod.NORTH_AMERICA))
    
    def now(self) -> datetime:
        pass

    def wait_until_next_prayer(self):
        pass

    def play_athan(self):
        pass

    def get_next_prayer_time(self) -> datetime:
        reference_time = self.now().astimezone()

        prayer_times = PrayerTimes(
            self.coordinates, reference_time, CalculationMethod.NORTH_AMERICA
        )

        if reference_time < prayer_times.fajr:
            return prayer_times.fajr

        if reference_time < prayer_times.dhuhr:
            return prayer_times.dhuhr

        if reference_time < prayer_times.asr:
            return prayer_times.asr

        if reference_time < prayer_times.maghrib:
            return prayer_times.maghrib

        if reference_time < prayer_times.isha:
            return prayer_times.isha

        next_day = reference_time + timedelta(days=1)
        prayer_times = PrayerTimes(
            self.coordinates, next_day, CalculationMethod.NORTH_AMERICA
        )
        self.print_prayer_times(next_day, prayer_times)
        return prayer_times.fajr

    def print_prayer_times(self, when: datetime, prayer_times: PrayerTimes):
        dateformat = "%H:%M"
        print(f"\n\nPrayer times for {when.strftime('%A %d %B %Y')}:")
        print(f"Fajr:    {prayer_times.fajr.astimezone().strftime(dateformat)}")
        print(f"Sunrise: {prayer_times.sunrise.astimezone().strftime(dateformat)}")
        print(f"Dhuhr:   {prayer_times.dhuhr.astimezone().strftime(dateformat)}")
        print(f"Asr:     {prayer_times.asr.astimezone().strftime(dateformat)}")
        print(f"Maghrib: {prayer_times.maghrib.astimezone().strftime(dateformat)}")
        print(f"Isha:    {prayer_times.isha.astimezone().strftime(dateformat)}\n")


class DryRunCalculator(PrayerTimeCalculator):
    def __init__(self, coordinates: tuple[float, float]):
        self.time = datetime.now().astimezone()
        super().__init__(coordinates)
        print(f"Press Enter to skip to the next prayer time. Current time is {self.time}")

    def now(self) -> datetime:
        return self.time

    def wait_until_next_prayer(self):
        input()
        next_prayer_time = self.get_next_prayer_time()
        self.time = next_prayer_time
        print(f"Next prayer time is at {next_prayer_time.astimezone()}")


class RealTimePrayerTimes(PrayerTimeCalculator):
    def __init__(self, coordinates: tuple[float, float], athan_sound: pygame.mixer.Sound):
        super().__init__(coordinates)
        self.athan_sound = athan_sound

    def now(self) -> datetime:
        return datetime.now().astimezone()

    def wait_until_next_prayer(self):
        next_prayer_time = self.get_next_prayer_time()
        print(f"Next prayer time is at {next_prayer_time.astimezone()}")
        sleep((next_prayer_time - self.now()).total_seconds())

    def play_athan(self):
        self.athan_sound.play()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A program meant to run continuously in the background, playing the athan at" \
        "the appropriate prayer times. The prayer times will be calculated either from the" \
        "computers IP address or from a provided latitude and longitude value"
    )
    parser.add_argument("athan_sound_file")
    parser.add_argument("--latlon", help="The latitude and longitude of the location for athan times, in format lat,lon")
    parser.add_argument("--dryrun", help="Dry run mode to see if the prayer times are calculated correctly", action="store_true")
    args = parser.parse_args()


    if (args.latlon is not None):
        coordinates = tuple(map(float, args.latlon.split(',')))
        print(f"Using provided coordinates: {coordinates}")
    else:
        g = geocoder.ip('me')
        coordinates = (g.lat, g.lng)
        print(f"Using geolocated coordinates from IP: {coordinates}")

    if args.dryrun:
        prayer_times = DryRunCalculator(coordinates)
    else:
        pygame.init()
        pygame.mixer.init()
        athan_sound = pygame.mixer.Sound(args.athan_sound_file)
        athan_sound.set_volume(1.0)
        prayer_times = RealTimePrayerTimes(coordinates, athan_sound)

    while True:
        prayer_times.wait_until_next_prayer()
        prayer_times.play_athan()
