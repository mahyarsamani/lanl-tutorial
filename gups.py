# Copyright (c) 2021 The Regents of the University of California
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
This scripts is used for checking the correctness of statistics reported
by the gem5 simulator. It can excercise certain components in the memory
subsystem. The reported values could be used to compare against a validated
set of statistics.
"""

import m5

from m5.objects import Root
from gem5.components.boards.test_board import TestBoard

from gem5.components.processors.gups_generator import GUPSGenerator

from gem5.components.cachehierarchies.ruby.mesi_two_level_cache_hierarchy \
    import MESITwoLevelCacheHierarchy
from gem5.components.memory import HBM2Stack


cache_hierarchy = MESITwoLevelCacheHierarchy(
                                            l1i_size="32KiB",
                                            l1i_assoc="8",
                                            l1d_size="32KiB",
                                            l1d_assoc="8",
                                            l2_size="256KiB",
                                            l2_assoc="4",
                                            num_l2_banks=16
                                            )

memory = HBM2Stack()
table_size = f"{int(memory.get_size() / 2)}"
generator = GUPSGenerator(0, table_size, update_limit=100000, clk_freq="5GHz")

# We use the Test Board. This is a special board to run traffic generation
# tasks
motherboard = TestBoard(
    clk_freq="5GHz",
    processor=generator,  # We pass the traffic generator as the processor.
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

root = Root(full_system=False, system=motherboard)

m5.instantiate()

generator.start_traffic()
print("Beginning simulation!")
exit_event = m5.simulate()
print(
    "Exiting @ tick {} because {}.".format(m5.curTick(), exit_event.getCause())
)
