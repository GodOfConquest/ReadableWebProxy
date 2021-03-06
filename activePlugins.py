


# Convenience functions to make intervals clearer.
def days(num):
	return 60*60*24*num
def hours(num):
	return 60*60*num
def minutes(num):
	return 60*num



# Plugins in this dictionary are the active plugins. Comment out a plugin to disable it.
# plugin keys specify when plugins will start, and cannot be duplicates.
# All they do is specify the order in which plugins
# are run, initially, starting after 1-minue*{key} intervals

import WebMirror.TimedTriggers.RssTrigger
import WebMirror.TimedTriggers.TimeoutTrigger
import WebMirror.TimedTriggers.PageTriggers

scrapePlugins = {
	0  : (WebMirror.TimedTriggers.RssTrigger.RssTriggerBase,                   minutes(30)),
	# 1  : (WebMirror.TimedTriggers.TimeoutTrigger.TimeoutTriggerBase,           minutes(31)),
	2  : (WebMirror.TimedTriggers.PageTriggers.HourlyPageTrigger,              minutes(60)),
	3  : (WebMirror.TimedTriggers.PageTriggers.EveryOtherDayPageTrigger,       days(2)),


}



import WebMirror.processor.HtmlProcessor
import WebMirror.processor.GDriveDirProcessor
import WebMirror.processor.GDocProcessor
import WebMirror.processor.MarkdownProcessor
import WebMirror.processor.BinaryProcessor
import WebMirror.processor.RssProcessor
import WebMirror.processor.WattPadJsonProcessor

PLUGINS = [
	WebMirror.processor.HtmlProcessor.HtmlPageProcessor,
	WebMirror.processor.GDriveDirProcessor.GDriveDirProcessor,
	WebMirror.processor.GDocProcessor.GdocPageProcessor,
	WebMirror.processor.MarkdownProcessor.MarkdownProcessor,
	WebMirror.processor.BinaryProcessor.BinaryResourceProcessor,
	WebMirror.processor.RssProcessor.RssProcessor,
	WebMirror.processor.WattPadJsonProcessor.WattPadJsonProcessor,
]


import WebMirror.OutputFilters.RoyalRoadL.RRLSeriesPageFilter
import WebMirror.OutputFilters.RoyalRoadL.RRLSeriesUpdateFilter
import WebMirror.OutputFilters.WattPad.WattPadSeriesPageFilter
import WebMirror.OutputFilters.JapTem.JapTemSeriesPageFilter
import WebMirror.OutputFilters.Booksie.BooksieSeriesPageFilter

FILTERS = [
	WebMirror.OutputFilters.RoyalRoadL.RRLSeriesPageFilter.RRLSeriesPageProcessor,
	WebMirror.OutputFilters.RoyalRoadL.RRLSeriesUpdateFilter.RRLSeriesUpdateFilter,
	WebMirror.OutputFilters.JapTem.JapTemSeriesPageFilter.JapTemSeriesPageProcessor,
	WebMirror.OutputFilters.Booksie.BooksieSeriesPageFilter.BooksieSeriesPageProcessor,
]


import WebMirror.OutputFilters.WattPad.WattPadInit

INIT_CALLS = [
	WebMirror.OutputFilters.WattPad.WattPadInit.init_call
]

print("Processing plugins: %s, active filters: %s, trigger plugins: %s" % (len(PLUGINS), len(FILTERS), len(scrapePlugins)))
