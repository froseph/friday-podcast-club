---
## Important: If this is a draft, next line should NOT begin with #
# draft: true
title: "{{{episode}}} - {{{podcast}}}"
date: {{{post_date}}}
## below are user-defined parameters (lower case keys recommended)
episode: "{{{episode}}}"
podcasts: "{{{podcast}}}"
subtitle:
tags:
{{#tags}}
  - {{{.}}}
{{/tags}}
---

## Meeting Information

Podcast Episode
:   {{{episode}}} - {{{podcast}}}

Date
:   {{{meeting_date}}}

Time
:   5:30pm - 7:30pm PST

## Podcast Sources

{{#sources}}
{{{source}}}
:   {{{url}}}

{{/sources}}
