#![allow(dead_code)]
//! Module containing the MOSS readout protocol and basic structures to analyze the data.
pub mod moss_hit;
pub mod moss_packet;
pub mod test_util;
pub use moss_hit::MossHit;
pub use moss_packet::MossPacket;

use std::ops::RangeInclusive;

#[derive(Debug, PartialEq)]
pub(crate) enum MossWord {
    Idle,
    UnitFrameHeader,
    UnitFrameTrailer,
    RegionHeader,
    Data0,
    Data1,
    Data2,
    Delimiter,
    ProtocolError,
}

impl MossWord {
    pub(super) const IDLE_NO_BACKBONE: u8 = 0xFF; // 1111_1111 (default), used in long edge readout
    pub(super) const IDLE_FOUR_BIT: u8 = 0xF0; // 1111_0000, LEC readout 4-bit DMU mode
    pub(super) const IDLE_TWO_BIT: u8 = 0xFC; // 1111_1100, LEC readout 2-bit DMU mode
    pub(super) const IDLE_ONE_BIT: u8 = 0xFE; // 1111_1110, LEC readout 1-bit DMU mode
                                      // pub(super) const UNIT_FRAME_HEADER_LOWEST_ID: u8 = 0b1101_0001; // 1101_<unit_id[3:0]>
    pub(super) const UNIT_FRAME_TRAILER: u8 = 0b1110_0000; // 1110_0000
    pub(super) const REGION_HEADER: u8 = 0b1100_0000; // 1100_00_<region_id[1:0]>
    pub(super) const DATA_0: u8 = 0b0000_0000; // 00_<hit_row_pos[8:3]>
    pub(super) const DATA_1: u8 = 0b0100_0000; // 01_<hit_row_pos[2:0]>_<hit_col_pos[8:6]>
    pub(super) const DATA_2: u8 = 0b1000_0000; // 10_<hit_col_pos[5:0]>
    pub(super) const DELIMITER: u8 = 0xFA; // Not actually part of the MOSS protocol and could be subject to change (FPGA implementation detail)
    pub(crate) const UNIT_FRAME_HEADER_RANGE: RangeInclusive<u8> = 0xD1..=0xDA;
    pub(crate) const DATA_0_RANGE: RangeInclusive<u8> = 0..=0b0010_1000; // Max is 320 pixel on bottom regions
    pub(crate) const DATA_1_RANGE: RangeInclusive<u8> = 0b0100_0000..=0b0111_1101; // Max is 320 pixel on bottom regions
    pub(crate) const DATA_2_RANGE: RangeInclusive<u8> = 0b1000_0000..=0b1011_1111;

    pub fn from_byte(b: u8) -> MossWord {
        match b {
            // Exact matches
            Self::IDLE_NO_BACKBONE => MossWord::Idle,
            Self::IDLE_FOUR_BIT => MossWord::Idle,
            Self::IDLE_TWO_BIT => MossWord::Idle,
            Self::IDLE_ONE_BIT => MossWord::Idle,
            Self::UNIT_FRAME_TRAILER => MossWord::UnitFrameTrailer,
            six_msb if six_msb & 0xFC == Self::REGION_HEADER => MossWord::RegionHeader,
            four_msb if four_msb & 0xF0 == 0b1101_0000 => MossWord::UnitFrameHeader,
            Self::DELIMITER => Self::Delimiter,
            two_msb if two_msb & 0b1100_0000 == Self::DATA_0 => MossWord::Data0,
            two_msb if two_msb & 0b1100_0000 == Self::DATA_1 => MossWord::Data1,
            two_msb if two_msb & 0b1100_0000 == Self::DATA_2 => MossWord::Data2,
            _ => MossWord::ProtocolError,
        }
    }
}
