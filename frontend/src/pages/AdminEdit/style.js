import styled from 'styled-components';
import { Link } from 'react-router-dom';
import { darkPurple } from '../../constants/colors';

const bgPage = '#F5F7FB';
const card = '#FFFFFF';
const cardSoft = '#F6F7FB';
const border = '#E5E7EB';
const borderStrong = '#D1D5DB';
const text = '#0F172A';
const muted = '#6B7280';
const muted2 = '#9CA3AF';
const accent = darkPurple;
const accentAlt = '#0F766E';
const success = '#16A34A';
const danger = '#EF4444';
const warning = '#F59E0B';

const shadowSm = '0 10px 40px rgba(15, 23, 42, 0.08)';
const shadowSoft = '0 30px 80px rgba(15, 23, 42, 0.06)';

export const Container = styled.div`
  min-height: 100vh;
  background: radial-gradient(120% 60% at 20% 10%, #e9e2ff 0%, rgba(233, 226, 255, 0) 60%),
    radial-gradient(100% 40% at 80% 0%, #d8f5ef 0%, rgba(216, 245, 239, 0) 60%),
    ${bgPage};
  display: flex;
  flex-direction: column;
`;

// HEADER
export const Header = styled.header`
  position: sticky;
  top: 0;
  z-index: 10;
  backdrop-filter: blur(14px);
  background: rgba(255, 255, 255, 0.92);
  border-bottom: 1px solid ${border};
  box-shadow: 0 12px 24px rgba(15, 23, 42, 0.04);
`;

export const HeaderContent = styled.div`
  height: 72px;
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 20px;
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 16px;
`;

export const LogoImage = styled.img`
  height: 34px;
  width: auto;
`;

export const NavMenu = styled.nav`
  display: flex;
  gap: 8px;
  justify-self: center;
  background: rgba(241, 245, 249, 0.6);
  padding: 4px;
  border-radius: 12px;
  border: 1px solid ${border};
`;

export const NavItem = styled(Link)`
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  color: ${(props) => (props.$active ? accent : muted)};
  background: ${(props) => (props.$active ? '#FFFFFF' : 'transparent')};
  padding: 8px 16px;
  border-radius: 8px;
  transition: all 0.2s ease;
  box-shadow: ${(props) => (props.$active ? '0 2px 8px rgba(0,0,0,0.04)' : 'none')};

  &:hover {
    color: ${accent};
    background: ${(props) => (props.$active ? '#FFFFFF' : 'rgba(255,255,255,0.5)')};
  }
`;

export const UserProfile = styled(Link)`
  display: flex;
  align-items: center;
  gap: 12px;
  text-align: right;
  border-left: 1px solid ${border};
  padding-left: 16px;
  text-decoration: none;
  cursor: pointer;
  color: inherit;

  &:hover {
    opacity: 0.8;
  }
`;

export const UserName = styled.div`
  font-weight: 800;
  font-size: 13px;
  color: ${text};
  line-height: 1.1;
`;

export const UserRole = styled.div`
  font-size: 12px;
  color: ${muted};
  line-height: 1.1;
`;

export const UserAvatar = styled.img`
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
`;

// MAIN
export const MainContent = styled.main`
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
  padding: 32px 20px 48px;
  display: flex;
  flex-direction: column;
  gap: 24px;

  @media (min-width: 768px) {
    padding: 40px 20px 56px;
    gap: 28px;
  }
`;

export const TopBar = styled.div`
  display: flex;
  flex-direction: column;
  gap: 6px;
  color: ${muted};
`;

export const SectionBadge = styled.span`
  display: inline-flex;
  align-items: center;
  gap: 8px;
  width: fit-content;
  padding: 8px 12px;
  border-radius: 999px;
  background: rgba(106, 58, 159, 0.1);
  color: ${accent};
  font-weight: 800;
  font-size: 12px;
  letter-spacing: 0.01em;
  text-transform: uppercase;
`;

export const SectionMeta = styled.span`
  font-size: 13px;
  font-weight: 700;
  color: ${muted};
`;

export const Hero = styled.div`
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding: 20px;
  background: ${card};
  border: 1px solid ${border};
  border-radius: 16px;
  box-shadow: ${shadowSoft};

  @media (min-width: 960px) {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
`;

export const MetaRow = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
  margin-bottom: 6px;
`;

export const MetaLabel = styled.span`
  font-size: 12px;
  color: ${muted};
  font-weight: 800;
`;

export const MetaValue = styled.span`
  font-size: 12px;
  color: ${text};
  font-weight: 800;
`;

export const PageTitle = styled.h1`
  font-size: 30px;
  color: ${text};
  font-weight: 900;
  margin: 0;
  letter-spacing: -0.03em;

  @media (min-width: 768px) {
    font-size: 34px;
  }
`;

export const PageSubtitle = styled.p`
  margin: 0;
  font-size: 15px;
  color: ${muted};
  line-height: 1.5;
  max-width: 780px;
`;

export const Actions = styled.div`
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: flex-start;
`;

export const PrimaryButton = styled.button`
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(120deg, ${accent}, #8b5cf6);
  color: white;
  border: 1px solid rgba(0, 0, 0, 0.06);
  padding: 12px 16px;
  border-radius: 12px;
  font-weight: 800;
  font-size: 14px;
  cursor: pointer;
  transition: transform 0.12s ease, box-shadow 0.12s ease, opacity 0.12s ease;
  box-shadow: ${shadowSm};

  &:hover {
    transform: translateY(-1px);
    opacity: 0.98;
  }

  &:active {
    transform: translateY(0);
    opacity: 0.95;
  }

  &:focus-visible {
    outline: none;
    box-shadow: 0 0 0 3px rgba(107, 46, 158, 0.24), ${shadowSm};
  }
`;

export const GhostButton = styled.button`
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 14px;
  border-radius: 12px;
  border: 1px solid ${borderStrong};
  background: rgba(255, 255, 255, 0.8);
  font-weight: 800;
  color: ${text};
  cursor: pointer;
  transition: transform 0.12s ease, box-shadow 0.12s ease, border-color 0.12s ease;

  &:hover {
    transform: translateY(-1px);
    border-color: ${accent};
    box-shadow: ${shadowSm};
  }

  &:focus-visible {
    outline: none;
    box-shadow: 0 0 0 3px rgba(107, 46, 158, 0.18), ${shadowSm};
  }
`;

// STATS
export const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr;
  gap: 14px;

  @media (min-width: 640px) {
    grid-template-columns: repeat(4, 1fr);
  }
`;

export const StatCard = styled.div`
  display: flex;
  gap: 12px;
  padding: 16px;
  border-radius: 14px;
  border: 1px solid ${border};
  background: ${card};
  box-shadow: ${shadowSm};
  align-items: center;
`;

export const StatIcon = styled.div`
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background: linear-gradient(135deg, rgba(106, 58, 159, 0.12), rgba(14, 165, 233, 0.12));
  display: flex;
  align-items: center;
  justify-content: center;
  color: ${accent};
  border: 1px solid rgba(106, 58, 159, 0.18);
`;

export const StatLabel = styled.span`
  font-size: 12px;
  color: ${muted};
  font-weight: 800;
`;

export const StatValue = styled.div`
  font-size: 20px;
  font-weight: 900;
  color: ${text};
  letter-spacing: -0.02em;
`;

// SECTIONS
export const SectionCard = styled.section`
  background: ${card};
  border: 1px solid ${border};
  border-radius: 18px;
  box-shadow: ${shadowSoft};
  padding: 18px;

  @media (min-width: 768px) {
    padding: 20px;
  }
`;

export const SectionHeader = styled.div`
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: flex-start;
  margin-bottom: 12px;
  flex-wrap: wrap;
`;

export const SectionTitle = styled.h2`
  font-size: 18px;
  font-weight: 900;
  color: ${text};
  margin: 0;
  letter-spacing: -0.01em;
`;

export const SectionSubtitle = styled.p`
  margin: 4px 0 0;
  color: ${muted};
  font-size: 13px;
  line-height: 1.45;
`;

export const ItemList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 12px;
`;

export const ItemRow = styled.div`
  border: 1px solid ${border};
  background: ${cardSoft};
  border-radius: 14px;
  padding: 14px;
  display: grid;
  grid-template-columns: 1.6fr 1fr;
  gap: 12px;
  align-items: center;

  @media (max-width: 700px) {
    grid-template-columns: 1fr;
  }
`;

export const ItemName = styled.div`
  font-weight: 900;
  font-size: 14px;
  color: ${text};
  letter-spacing: -0.01em;
`;

export const ItemMeta = styled.div`
  font-size: 13px;
  color: ${muted};
  font-weight: 700;
  margin-top: 4px;

  strong {
    color: ${text};
  }
`;

export const ProgressBar = styled.div`
  width: 100%;
  height: 8px;
  background: #eef0f2;
  border-radius: 999px;
  overflow: hidden;
  margin: 8px 0 6px;
`;

export const ProgressFill = styled.div`
  height: 100%;
  width: 0%;
  background: linear-gradient(90deg, ${accent}, ${accentAlt});
  border-radius: 999px;
`;

// CANDIDATES
export const CandidateSection = styled.section`
  background: ${card};
  border: 1px solid ${border};
  border-radius: 18px;
  box-shadow: ${shadowSoft};
  padding: 18px;

  @media (min-width: 768px) {
    padding: 20px;
  }
`;

export const CandidateHeaderRow = styled.div`
  display: grid;
  grid-template-columns: 1.2fr 1fr 1fr 1fr 0.6fr;
  padding: 10px 12px;
  background: ${cardSoft};
  border: 1px solid ${border};
  border-radius: 12px;
  color: ${muted};
  font-weight: 800;
  font-size: 12px;
  margin-bottom: 12px;
`;

export const CandidateRow = styled.div`
  display: grid;
  grid-template-columns: 1.2fr 1fr 1fr 1fr 0.6fr;
  padding: 14px 12px;
  align-items: center;
  border-bottom: 1px solid ${border};

  &:last-child {
    border-bottom: none;
  }
`;

export const CandidateCell = styled.div`
  display: flex;
  align-items: center;
  gap: 6px;
  color: ${(props) => (props.$muted ? muted : text)};
  justify-content: ${(props) => (props.align === 'right' ? 'flex-end' : 'flex-start')};
  text-align: ${(props) => (props.align === 'right' ? 'right' : 'left')};
  font-weight: 700;
`;

export const CandidateInfo = styled.div`
  display: flex;
  flex-direction: column;
  gap: 4px;
`;

export const CandidateName = styled.span`
  font-weight: 900;
  color: ${text};
`;

export const CandidateTag = styled.span`
  font-size: 12px;
  color: ${muted};
  font-weight: 700;
`;

export const StatusBadge = styled.span`
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 900;
  width: fit-content;

  background-color: ${(props) =>
    props.$tone === 'success'
      ? 'rgba(22, 163, 74, 0.14)'
      : props.$tone === 'error'
      ? 'rgba(239, 68, 68, 0.12)'
      : 'rgba(245, 158, 11, 0.16)'};
  color: ${(props) =>
    props.$tone === 'success' ? success : props.$tone === 'error' ? danger : warning};
  border: 1px solid rgba(0, 0, 0, 0.04);
`;

export const PillButton = styled.button`
  padding: 10px 12px;
  border-radius: 12px;
  border: 1px solid ${border};
  background: ${card};
  color: ${text};
  font-weight: 800;
  cursor: pointer;
  transition: transform 0.12s ease, box-shadow 0.12s ease, border-color 0.12s ease;

  &:hover {
    transform: translateY(-1px);
    border-color: ${accent};
    color: ${accent};
    box-shadow: ${shadowSm};
  }

  &:focus-visible {
    outline: none;
    box-shadow: 0 0 0 3px rgba(107, 46, 158, 0.14);
  }
`;

// EMPTY
export const EmptyState = styled.div`
  padding: 28px 14px;
  text-align: center;
  color: ${muted};
  font-weight: 700;
`;

export const EmptyTitle = styled.h3`
  margin: 0 0 6px;
  font-size: 18px;
  font-weight: 900;
  color: ${text};
`;

export const EmptyText = styled.p`
  margin: 0;
  color: ${muted};
  font-size: 14px;
`;

export const StatusBadgeThin = styled.span`
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 7px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 900;
  width: fit-content;

  background: rgba(106, 58, 159, 0.08);
  color: ${accent};
`;
