### SPDX-License-Identifier: LGPL-3.0-only

example_desc = An example command.
example_text = Hello { $username }! This is an example command.
example_text1 = It {
    CHECK_WEEK_DAY(1) ->
        [true] is
        *[false] is not
} Monday.
