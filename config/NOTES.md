# CONFIGURATION NOTES

## Operations team configuration.

(M. Simpson, 11/10/2016)

Note that the canon service tree document is the XMind mind map ("operations_service_tree.xmind").

The configuration file used by IReportedThis, "operations_service_tree.yaml", is derived manually
from the XMind document -- there may be a way to automate this, but I haven't had time to get to
it yet.  The XMind format is XML-based, so there's probably a way forward there.

The simplified Markdown ("operations_service_tree.md") and tags-only ("operations_service_tree_tagsonly.txt")
documents are derived from the YAML configuration file via the "exsch" utility.

The population filter file ("operations_filter_working.md") is used to do some basic tag cleanup
and transformation as part of running the monthly reports.
