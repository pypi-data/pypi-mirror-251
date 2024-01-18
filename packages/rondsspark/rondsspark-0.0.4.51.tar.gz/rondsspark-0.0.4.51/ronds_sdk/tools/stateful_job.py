import datetime
import logging
import random

import schedule

logger = logging.getLogger("executor")


class StatefulJobs(schedule.Job):

    def __init__(self, interval: int, scheduler: schedule.Scheduler = None):
        super(StatefulJobs, self).__init__(interval, scheduler)

    def run(self):
        """
        Run the job and immediately reschedule it.
        If the job's deadline is reached (configured using .until()), the job is not
        run and CancelJob is returned immediately. If the next scheduled run exceeds
        the job's deadline, CancelJob is returned after the execution. In this latter
        case CancelJob takes priority over any other returned value.

        :return: The return value returned by the `job_func`, or CancelJob if the job's
                 deadline is reached.

        """
        if self._is_overdue(datetime.datetime.now()):
            logger.debug("Cancelling job %s", self)
            return schedule.CancelJob

        logger.debug("Running job %s", self)
        ret = self.job_func()
        self.last_run = datetime.datetime.now()
        self._schedule_next_run()

        if self._is_overdue(self.next_run):
            logger.debug("Cancelling job %s", self)
            return schedule.CancelJob
        return ret

    def _schedule_next_run(self) -> None:
        """
        Compute the instant when this job should run next.
        """
        if self.unit not in ("seconds", "minutes", "hours", "days", "weeks"):
            raise schedule.ScheduleValueError(
                "Invalid unit (valid units are `seconds`, `minutes`, `hours`, "
                "`days`, and `weeks`)"
            )

        if self.latest is not None:
            if not (self.latest >= self.interval):
                raise schedule.ScheduleError("`latest` is greater than `interval`")
            interval = random.randint(self.interval, self.latest)
        else:
            interval = self.interval

        self.period = datetime.timedelta(**{self.unit: interval})
        self.next_run = datetime.datetime.now() + self.period
        if self.start_day is not None:
            if self.unit != "weeks":
                raise schedule.ScheduleValueError("`unit` should be 'weeks'")
            weekdays = (
                "monday",
                "tuesday",
                "wednesday",
                "thursday",
                "friday",
                "saturday",
                "sunday",
            )
            if self.start_day not in weekdays:
                raise schedule.ScheduleValueError(
                    "Invalid start day (valid start days are {})".format(weekdays)
                )
            weekday = weekdays.index(self.start_day)
            days_ahead = weekday - self.next_run.weekday()
            if days_ahead <= 0:  # Target day already happened this week
                days_ahead += 7
            self.next_run += datetime.timedelta(days_ahead) - self.period
        if self.at_time is not None:
            if self.unit not in ("days", "hours", "minutes") and self.start_day is None:
                raise schedule.ScheduleValueError("Invalid unit without specifying start day")
            kwargs = {"second": self.at_time.second, "microsecond": 0}
            if self.unit == "days" or self.start_day is not None:
                kwargs["hour"] = self.at_time.hour
            if self.unit in ["days", "hours"] or self.start_day is not None:
                kwargs["minute"] = self.at_time.minute
            self.next_run = self.next_run.replace(**kwargs)  # type: ignore
            # Make sure we run at the specified time *today* (or *this hour*)
            # as well. This accounts for when a job takes so long it finished
            # in the next period.
            if not self.last_run or (self.next_run - self.last_run) > self.period:
                now = datetime.datetime.now()
                if (
                    self.unit == "days"
                    and self.at_time > now.time()
                    and self.interval == 1
                ):
                    self.next_run = self.next_run - datetime.timedelta(days=1)
                elif self.unit == "hours" and (
                    self.at_time.minute > now.minute
                    or (
                        self.at_time.minute == now.minute
                        and self.at_time.second > now.second
                    )
                ):
                    self.next_run = self.next_run - datetime.timedelta(hours=1)
                elif self.unit == "minutes" and self.at_time.second > now.second:
                    self.next_run = self.next_run - datetime.timedelta(minutes=1)
        if self.start_day is not None and self.at_time is not None:
            # Let's see if we will still make that time we specified today
            if (self.next_run - datetime.datetime.now()).days >= 7:
                self.next_run -= self.period
